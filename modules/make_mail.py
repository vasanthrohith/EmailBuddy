from modules.call_llm import Call_LLM
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 
from typing import Annotated, Dict, TypedDict
from langgraph.graph import END, StateGraph
import re

class mail_json_eval(BaseModel):
    subject: str = Field(description="Subject of the mail")
    mail_body: str = Field(description="Only body of the mail")
    # mail_closing: str = Field(description="a concluding remark, followed by their name alone")

class GraphState(TypedDict):
        """
        Represents the state of our graph.

        Attributes:
            keys: A dictionary where each key is a string.
        """
        keys: Dict[str, any]


class CorrectGraph(Call_LLM):
    def __init__(self):
        super().__init__()

    def get_template(self, make_prof_mail_temp=None, summarize_content_temp=None):
        if make_prof_mail_temp:
            make_prof_mail_temp ="""
                with the given content convert this to a professional mail:\n
                
                Recipient's Name : {recipient_name}\n
                Sender name : {sender_name}\n           
                content : {user_content}\n

                note: use the above Sender name and Recipient's Name in the mail.

                your response should be in the below format:

                 \n{format_instructions}\n

            """

            return make_prof_mail_temp
        
        elif summarize_content_temp:
            summarize_content_temp = """

                You need to summarize the below content in more detailed manner without changing the context

                content : {content}

            """
            return summarize_content_temp

    # def write_formal_mail(self, user_content, recipient_name, sender_name):
    def write_formal_mail(self, state):
        print("--write_formal_mail--")
        state_dict = state['keys']
        # print()
        # print(state_dict['user_content'])
        user_content= state_dict['user_content']
        recipient_name = state_dict['recipient_name']
        sender_name = state_dict['sender_name']

        # try:
        parser = JsonOutputParser(pydantic_object=mail_json_eval)

        make_mail_prompt = PromptTemplate(
        template=self.get_template(make_prof_mail_temp=True),
        input_variables=["user_content","recipient_name","sender_name"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # print(make_mail_prompt.invoke({"user_content":user_content}))

        try:
            make_mail_chain = make_mail_prompt | self.llm | parser

            make_mail_response = make_mail_chain.invoke({"user_content":user_content,"recipient_name":recipient_name,"sender_name":sender_name})
            
            print("make_mail_response : ",make_mail_response)

            return {"keys":{"make_mail_response":make_mail_response, "status":"good"}}

        except Exception as error:
            print("Exception in Node : write_formal_mail >>> ", error)
            state['keys']["status"]="bad"
            return state
        
    def summarize_content(self, content):
        print("--summarize_content--")
        summarize_prompt = PromptTemplate(
        template=self.get_template(summarize_content_temp=True),
        input_variables=["content"],
        )

        try:
            summarize_chain = summarize_prompt | self.llm 
            return summarize_chain.invoke({"content":content})

        except Exception as error:
            print("Exception in summarize_content >>>",error)

    def decision_node(self, state):
        print("--decision_node--")
        state_dict = state['keys']
        # print(state)

        if state_dict['status']=="good":
            return "__end__"
        
        elif state_dict['status']=="bad":
            summarized_content = self.summarize_content(content=state_dict['user_content'])
            state['keys']['user_content']=summarized_content

            return "write_formal_mail"

    def run_nodes(self, GraphState):
        print("--run_nodes--")
        workflow = StateGraph(GraphState)

        workflow.add_node("write_formal_mail", self.write_formal_mail)

        print("building graph...")
        workflow.set_entry_point("write_formal_mail")

        workflow.add_conditional_edges(
            "write_formal_mail",
            self.decision_node
        )

        print("Running app...")

        self.app = workflow.compile()

    def start_process(self, user_content, recipient_name, sender_name):
        print("--start_process--")

        self.run_nodes(GraphState)

        print("--invoking app--")

        response = self.app.invoke({"keys":{"user_content":user_content, "recipient_name":recipient_name, "sender_name":sender_name}})
        print("node response >>> ", response)

        return response



class MakeMail(CorrectGraph):
    def __init__(self):
        super().__init__()


    def extract_name(self, email):
        # Regular expression to match letters before any numbers in the email's local part
        match = re.match(r'^([a-zA-Z]+)', email)
        if match:
            return match.group(1)
        else:
            return None

    # Example usage
    # email = "vasanth777@gmail.com"
    # name = extract_name(email)
    # print(name)  # Output: vasanth


    def Make_Formal_Mail(self, user_content, recipient_mail, sender_mail):
        print("--Make_Formal_Mail--")

        recipient_name = self.extract_name(email=recipient_mail)
        sender_name = self.extract_name(email=sender_mail)
        print("recipient_name >>> ", recipient_name)
        print("sender_name >>> ", sender_name)
        mail_generated = self.start_process(user_content, recipient_name, sender_name)

        return mail_generated['keys']

# obj=MakeMail()
# obj.Make_Formal_Mail(user_content="I want to take a leave for my aunt's wedding, I'll connect with team whenever needed i need 2 weeks work from home", recipient_mail="vasanth.s@valuehealthsol.com", sender_mail="vasanthrohith777@gmail.com")




