import gradio as gr
import requests


def generate_response(question,context,model):
    URL="http://0.0.0.0:8003/get_ollama_response"
    data= {"context":context,"question":question,"model":model}
    response= requests.post(URL, json=data)
    print(f"response \n {response}")
    if response.status_code==200:
        return response.json()['response']
    return "Failed to connect the server!!!"


def submit_rating(response_text,rating):
    if rating is not None and response_text !="":
        URL="http://0.0.0.0:8003/insert_rating"
        data={"response":response_text,"rating":rating}
        response= requests.post(URL, json=data)
        if response.status_code==200:
            return "Rating submitted successfully"
        return "Failed to submit ratings!!!"
    else:
        return "No rating submitted"

with gr.Blocks() as iface:
    with gr.Row():
        context_input = gr.Textbox(label="Context")
        question_input = gr.Textbox(label="User Question")
        model_input = gr.Dropdown(label="Model", choices=["llama3.2:latest", "llama2:latest", "mistral:latest", "phi3:latest","gemma:latest"])
        submit_btn = gr.Button("Generate Response")

    response_output = gr.Textbox(label="Response", interactive=False)
    rating_input = gr.Slider(label="Rate the response", minimum=1, maximum=5, step=1)
    rating_btn = gr.Button("Submit Rating")
    rating_output = gr.Label()

    submit_btn.click(
        generate_response,
        inputs=[context_input, question_input, model_input],
        outputs=[response_output]
    )

    rating_btn.click(
        submit_rating,
        inputs=[response_output, rating_input],
        outputs=rating_output
    )

iface.launch()


