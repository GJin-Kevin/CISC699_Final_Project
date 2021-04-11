import matplotlib.pyplot as plt


class Visualization:

    def __init__(self, df):
        self.df = df

    
    def sma_plot_result(self):
    
        plt.style.use('seaborn-whitegrid')
        #plt.figure(figsize=(10,6))
        
        plt.plot_date(self.df['date'], self.df['Profit'], 'c--', linestyle='solid', label = 'Strategy Performance', linewidth = 1)
        plt.plot_date(self.df['date'], self.df['Pct_change'], 'g-.', linestyle='solid', label = 'Stock Performance', linewidth = 1)

        plt.xlabel('Date', fontsize = 14)
        plt.ylabel('Percent', fontsize = 14)
        plt.title('BackTesting Result', fontsize = 16)

        plt.legend(fontsize = 12)

        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        plt.show()

    
    def rsi_plot_result(self):
    
        plt.style.use('seaborn-whitegrid')
        #plt.figure(figsize=(10,6))
        
        plt.plot_date(self.df['date'], self.df['Profit'], 'c--', linestyle='solid', label = 'Strategy Performance', linewidth = 1)
        plt.plot_date(self.df['date'], self.df['Pct_change'], 'g-.', linestyle='solid', label = 'Stock Performance', linewidth = 1)

        plt.xlabel('Date', fontsize = 14)
        plt.ylabel('Percent', fontsize = 14)
        plt.title('BackTesting Result', fontsize = 16)

        plt.legend(fontsize = 12)

        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        plt.show()

    
    def boll_plot_result(self):
        
        fig, axs = plt.subplots(2)
        plt.style.use('seaborn-whitegrid')
        #plt.figure(figsize=(10,6))
        
        # axs[0].plt.plot_date(self.df['date'], self.df['Profit'], 'c--', linestyle='solid', label = 'Strategy Performance', linewidth = 1)
        # axs[0].plt.plot_date(self.df['date'], self.df['Pct_change'], 'g-.', linestyle='solid', label = 'Stock Performance', linewidth = 1)

        # axs[1].plt.plot_date(self.df['date'], self.df['Upper'], 'k--', linestyle='solid', label = 'Upper Band', linewidth = 1)
        # axs[1].plt.plot_date(self.df['date'], self.df['Lower'], 'k--', linestyle='solid', label = 'Lower Band', linewidth = 1)
        # axs[1].plt.plot_date(self.df['date'], self.df['close'], 'r--', linestyle='solid', label = 'Upper Band', linewidth = 1)

        axs[0].plot_date(self.df['date'], self.df['Profit'], 'c--', linestyle='solid', label = 'Strategy Performance', linewidth = 1)
        axs[0].plot_date(self.df['date'], self.df['Pct_change'], 'g--', linestyle='solid', label = 'Stock Performance', linewidth = 1)

        axs[0].set(title = "BackTesting Result", xlabel = "Date", ylabel = "Percent")
        axs[0].legend(fontsize = 12)

        axs[1].plot_date(self.df['date'], self.df['Upper'], 'k--', linestyle='dotted', label = 'Upper Band', linewidth = 1)
        axs[1].plot_date(self.df['date'], self.df['Lower'], 'k--', linestyle='dotted', label = 'Lower Band', linewidth = 1)
        axs[1].plot_date(self.df['date'], self.df['close'], 'r--', linestyle='solid', label = 'Price', linewidth = 1)

        axs[1].set(title = "Stock Prices with Boll Bands", xlabel = "Date", ylabel = "Price")
        axs[1].legend(fontsize = 12)

        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        plt.show()