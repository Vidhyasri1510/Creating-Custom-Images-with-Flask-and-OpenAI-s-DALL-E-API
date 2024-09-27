from flask import Flask, render_template, request
import openai
import logging

app = Flask(__name__)

openai.api_key = 'YOUR_OPENAI_API_KEY'

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    error = None

    if request.method == 'POST':
        try:
            theme = request.form.get('theme')
            prompt = request.form.get('prompt')
            include_negative = 'include_negative' in request.form
            negative_prompt = request.form.get('negative_prompt') if include_negative else ""

            final_prompt = f"{theme} {prompt}"
            if negative_prompt:
                final_prompt += f" but avoid {negative_prompt}"


            response = openai.Image.create(
                prompt=final_prompt,
                n=1,
                size="256x256"
            )
            image_url = response['data'][0]['url']
        except Exception as e:
            logging.error("Error generating image: %s", str(e))
            error = str(e)

    return render_template('index.html', image_url=image_url, error=error)

if __name__ == '__main__':
    app.run(debug=True)