from flask import Flask, render_template, url_for, request, redirect
from OLXScraper import olx_scrapper


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_ = request.form['url']
        nop_ = int(request.form['nr_of_pages'])
        print('redirect to  result')
        return redirect(url_for("result", url=url_, nop=nop_))
    else:
        print('render index')
        return render_template('index.html', nop=1)


@app.route('/<int:nop>/<path:url>', methods=['GET', 'POST'])
def result(nop: int, url: str):
    if request.method == 'POST':
        url_ = request.form['url']
        nop_ = int(request.form['nr_of_pages'])
    else:
        url_ = url
        nop_ = nop
    try:
        df = olx_scrapper(url_, nr_of_page=nop_, url_to_hyperlink=True)
        return render_template('result.html', table=df.to_html(
            header="true", classes='styled-table', escape=False), nop=nop_, url_=url,)
    except Exception:
        return render_template('result.html', table=r'''<div class="w3-panel w3-red my-alert">
                               <h3>Uwaga</h3><p> Podany link jest nieprawidłowy lub nie da się go zescrapować (np zła kategoria: np. praca). </p>
                               </div>''',
                               nop=nop_, url_=url,)


if __name__ == '__main__':
    app.run()
