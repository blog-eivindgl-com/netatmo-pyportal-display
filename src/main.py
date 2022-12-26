import model.widget, model.display

def main():
    w1 = model.widget.Widget("temperature", "Stua", 22)
    w2 = model.widget.Widget("temperature", "Vestveggen", 7.5)
    d = model.display.Display()
    d.widgets.append(w1)
    d.widgets.append(w2)
    print(f"fine - {w1.type}, {w1.description}, {w1.value}")
    print(f"w2 {d.widgets.index(1).type}, {d.widgets.index(1).description}")

main()