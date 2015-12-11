from app import app

@app.template_filter()
def newline_to_linebreak(text):
    return text.replace('\n', '<br />\n')
