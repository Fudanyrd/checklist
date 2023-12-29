from flask import Flask, render_template, request

app = Flask(__name__)

def load_data(
    filename: str
) -> list:
    res = []
    with open(filename,'r') as fobj:
        rows = fobj.readlines()
        for row in rows:
            if len(row)>0:
                res.append(row)
    return res

def get_task(
    tasks: list,
    idx: int
) -> str:
    if len(tasks) <= idx:
        return "<Nothing to be done>"
    else:
        return tasks[idx]

def dump_data(
    filename: str,
    tasks: list
) -> None:
    with open(filename,'w') as fobj:
        for task in tasks:
            fobj.write(task)
            if not task[-1]=='\n':
                fobj.write('\n')
        fobj.close()

@app.route('/')
def main_page() -> str:
    tasks = load_data("tasks.txt")
    return render_template("main.html",task1=get_task(tasks,0),
        task2=get_task(tasks,1),task3=get_task(tasks,2),num=str(len(tasks)))

@app.route('/disp')
def disp_page() -> str:
    res = ""
    tasks = load_data("tasks.txt")
    try:
        num = int(request.args.get('num'))
    except ValueError:
        return render_template("failure.html")
    for i in range(num):
        res+=(str(i+1)+'. ')
        res += get_task(tasks,i)
        res += '\n'
    return render_template("display.html",tasks = res)

@app.route('/add')
def add_page() -> str:
    tasks = load_data("tasks.txt")
    new_task = request.args.get('add')
    tasks.append(new_task+'\n')
    dump_data("tasks.txt",tasks)
    return render_template("add.html",added = new_task,total = len(tasks))

@app.route('/temp')
def remove_temp() -> str:
    res = request.args.get('confirmation')
    if res != 'Y':
        return render_template("failure.html")
    res = ""
    tasks = load_data("tasks.txt")
    num = len(tasks)
    for i in range(num):
        res+=(str(i+1)+'. ')
        res += get_task(tasks,i)
        res += '\n'
    return render_template("temp.html",tasks = res)

@app.route('/remove')
def remove_task() -> str:
    tasks = load_data("tasks.txt")
    try:
        idx = int(request.args.get('idx')) - 1
    except ValueError:
        return render_template("failure.html")
    _removed = get_task(tasks,idx)
    try:
        tasks.remove(_removed)
    except ValueError:
        return render_template("failure.html")
    finally:
        dump_data("tasks.txt",tasks)
    return render_template("remove.html",removed=_removed,total=str(len(tasks)))
    