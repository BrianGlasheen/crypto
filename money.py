from coinmarketcap import Market
import tkinter as tk

class CryptoApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, MainPage, AboutPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont) -> None:

        frame = self.frames[cont]
        frame.tkraise()
      
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Crypto-Grid", font=("Verdana", 12))
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Crypto Currencies",
                            command=lambda: controller.show_frame(MainPage))
        button.pack()

        button2 = tk.Button(self, text="About",
                            command=lambda: controller.show_frame(AboutPage))
        button2.pack()

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.lable_exists = False

        self.canvas = tk.Canvas(self,)
        self.canvas.grid(row=1, column=0, columnspan=4)  

        scrollbar = tk.Scrollbar(self.canvas, command=self.canvas.yview)
        scrollbar.grid(row=0, column=7, rowspan=101, sticky=tk.NS) 
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.labels = []
        coin_range = 9
        self.create_grid(coin_range)

        label = tk.Label(self, text="Crypto-Grid", font=("Verdana", 12))
        label.grid(row=0, column=1, padx=10, sticky=tk.W)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, padx=10, sticky=tk.W)

        update_button = tk.Button(self, text="Update",
                                  command=lambda: self.coin_update(coin_range))
        update_button.grid(row=0, column=3, padx=10, sticky=tk.E)

        self.arg_entry = tk.Entry(self)
        self.arg_entry.grid(row=0, column=2, pady=10, sticky=tk.N)

    def create_grid(self, coin_range: int, inputs={}) -> None:

        """ Creates grid of labels, makes api call, calls on 
            parsing/building functions to create body of gui. 
            returns nothing. """
        
        self.clear_canvas()

        self.coinmarketcap = Market()

        start = int(inputs.get('start', 0))
        stop = int(inputs.get('stop', start+9))

        # start, stop = [(start, stop), (stop, start)][start > stop]
        start, stop = self.sort2(start, stop)

        if not start: 
            stop -= 1
        stop -= start-1

        coins = self.coinmarketcap.ticker(start=start, limit=stop)['data']
        attributes = ['rank', 'symbol', 'name', 'usd', 'total_supply', 'usd', 'usd']
        usd_attributes = ['price', 'percent_change_24h', 'percent_change_7d']
        
        if not self.lable_exists:
            self.create_grid_label(coins, attributes, usd_attributes)
            self.lable_exists = True
        self.create_grid_body(coins, attributes, usd_attributes)

    def create_grid_label(self, coins, attributes, usd_attributes) -> None:
        z = 0
        for i, v in enumerate(attributes):
            if v == 'usd':
                x = usd_attributes[z]
                l = tk.Label(self.canvas, text=f"{usd_attributes[z].replace('_', ' ').capitalize().replace('Percent', '%')}", relief=tk.RIDGE)
                l.grid(row=0, column=i, sticky=tk.NSEW)
                z += 1
            else:
                l = tk.Label(self.canvas, text=f"{v.replace('_', ' ').capitalize()}", relief=tk.RIDGE)
                l.grid(row=0, column=i, sticky=tk.NSEW)

    def create_grid_body(self, coins, attributes, usd_attributes) -> None:
        for i, coin in enumerate(coins):
            z = 0
            for j in range(7):
                if attributes[j] == 'usd':
                    x = usd_attributes[z]
                    atr = self.format_string(str(coins[coin]['quotes']['USD'][x]), x)
                    l = tk.Label(self.canvas, text=atr, relief=tk.RIDGE)
                    l.grid(row=i+1, column=j, sticky=tk.NSEW)
                    self.labels.append(l)
                    z += 1
                else:    
                    x = attributes[j]
                    atr = self.format_string(str(coins[coin][x]), x)
                    l = tk.Label(self.canvas, text=atr, relief=tk.RIDGE)
                    l.grid(row=i+1, column=j, sticky=tk.NSEW)
                    self.labels.append(l)

    def format_string(self, s: str, f: str) -> str:
        if f in ['price', 'total_supply']:
            return f"${round(float(s), 2)}"
        return s

    def coin_update(self, coin_range: int) -> None:
        inputs = self.input_cleaner(self.arg_entry.get())
        self.create_grid(coin_range, inputs)

    def input_cleaner(self, inputs: str) -> dict:
        if not inputs:
            return {}
        return dict((k.strip(), v.strip()) for k,v in (item.split('=') for item in inputs.split(';')))

    def clear_canvas(self) -> None:
        for l in self.labels:
            l.destroy()
    
    def sort2(self, a, b):
        if a < b:
            return a, b
        else:
            return b, a

class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Crypto-Grid Info", font=("Verdana", 12))
        label.pack(pady=5,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side="bottom", pady=5)

        main = tk.Text(self, wrap=tk.WORD, width=56, height=11)
        main.pack()
        main.tag_configure("center", justify='center')

        with open("text.txt", 'r') as txt:
            for line in txt:
                main.insert(tk.END, line)
        
        main.tag_add("center", 1.0, "end")
  
if __name__ == "__main__":
    app = CryptoApp()
    app.wm_title("Crypto-Grid")
    app.resizable(width=False, height=True)
    app.mainloop()