import tkinter as tk
from tkinter import messagebox, scrolledtext
from bot import login, query_user_specific
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

class DepotChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Depot AI ChatBot")

        self.user_context = None  # Holds user info after login

        # Login Frame
        self.login_frame = tk.Frame(root)
        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)

        self.username_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.attempt_login).grid(row=2, columnspan=2, pady=10)
        self.login_frame.pack(pady=20)

        # Chat Frame
        self.chat_frame = tk.Frame(root)
        self.chat_log = scrolledtext.ScrolledText(self.chat_frame, width=60, height=20, state='disabled')
        self.chat_log.pack(pady=10)

        self.user_input = tk.Entry(self.chat_frame, width=50)
        self.user_input.pack(side=tk.LEFT, padx=10)
        tk.Button(self.chat_frame, text="Send", command=self.send_message).pack(side=tk.LEFT)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_info = login(username, password)

        if user_info:
            self.user_context = user_info
            messagebox.showinfo("Success", "Login successful!")
            self.login_frame.pack_forget()
            self.chat_frame.pack()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def send_message(self):
        question = self.user_input.get()
        if question and self.user_context:
            self.chat_log.configure(state='normal')
            self.chat_log.insert(tk.END, f"You: {question}\n")
            self.chat_log.configure(state='disabled')
            self.user_input.delete(0, tk.END)

            try:
                raw_response = query_user_specific(question, self.user_context)
                output=raw_response.get("output","")
                summary_prompt = PromptTemplate.from_template(
                    "From the following input, extract and return only the final answer mentioned at the end — the text that comes after the last occurrence of 'Final Answer:'. Do not include any thoughts, SQL, or explanations make it frindly in nature and provide it in a conversational answer manner:\n\n{response}"
                )
                llm = ChatOllama(model="llama3.2", temperature=0)
                summarizer_chain = summary_prompt | llm
                answer = summarizer_chain.invoke({"response": output})


            except Exception as e:
                answer = f"Error: {e}"

            self.chat_log.configure(state='normal')
            self.chat_log.insert(tk.END, f"Bot: {answer.content if hasattr(answer, 'content') else answer}\n\n")
            self.chat_log.configure(state='disabled')
            self.chat_log.yview(tk.END)

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DepotChatBotGUI(root)
    root.mainloop()
