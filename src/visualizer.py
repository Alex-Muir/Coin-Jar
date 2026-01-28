import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    """A class for making visualizations of data"""

    def __init__(self):
        """Nothing happens here"""
        pass

    def pie_chart(self, data):
        """Generates a pie chart"""
        # For the labels and sizes of the pie chart
        labels = self._get_labels(data)
        sizes = self._get_sizes(data)

        # Show the pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.show()       

    def _get_labels(self, data):
        """Gets the names of the expense/income types to be used as labels"""
        labels = []
        for item in data:
            name = item[0]
            if name not in labels:
                labels.append(name)

        return labels

    def _get_sizes(self, data):
        """
        Get the sum of the expense/income type to be used for sizes of the pie 
        chart
        """
        sizes = []
        seen = set()
        for item in data:
            sum = 0
            name = item[0]
            if name in seen:
                continue
            for item in data:
                if name in item and name not in seen:
                    sum += item[2]
            seen.add(name)
            sizes.append(sum)

        return sizes

    def line_graph(self, data):
        """Generate Line Graph"""

        if data["line_graph_data"]:
            x = list(data["line_graph_data"].keys())
            y = list(data["line_graph_data"].values())
            low = data["low"] - 10
            high = data["high"] + 10

            fig, ax = plt.subplots()
            ax.plot(x, y, marker="o")
            ax.set_ylim(low, high)
            ax.set(xlabel="date", label="total")
            ax.grid()

            ax.set_title("Coin Jar Total")
            plt.show()
        else:
            print("There is not data")


