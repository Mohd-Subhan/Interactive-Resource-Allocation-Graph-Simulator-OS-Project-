import tkinter as tk
from tkinter import ttk, messagebox
from allocation import ResourceManager
from visualization import GraphVisualizer

class ResourceAllocationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive Resource Allocation Simulator")
        self.root.geometry("900x700")
        self.manager = ResourceManager()
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 11))

        # Create UI elements first
        self.create_widgets()

        # Initialize the visualizer after canvas creation
        self.visualizer = GraphVisualizer(self.manager, self.canvas)
        self.visualizer.show_graph()  # Initial graph display

    def create_widgets(self):
        """ Create the UI components """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        input_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Process:").grid(row=0, column=0, pady=5)
        self.process_entry = ttk.Entry(input_frame, width=15)
        self.process_entry.grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="Resource:").grid(row=1, column=0, pady=5)
        self.resource_entry = ttk.Entry(input_frame, width=15)
        self.resource_entry.grid(row=1, column=1, pady=5)

        ttk.Button(input_frame, text="Allocate", command=self.allocate_resource).grid(row=2, column=0, padx=5)
        ttk.Button(input_frame, text="Release", command=self.release_resource).grid(row=2, column=1, padx=5)
        ttk.Button(input_frame, text="Check Deadlock", command=self.check_deadlock).grid(row=3, column=0, padx=5)
        ttk.Button(input_frame, text="Clear Log", command=self.clear_log).grid(row=3, column=1, padx=5)

        # Create Canvas for Graph Visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="5")
        viz_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.S, tk.E))
        self.canvas = tk.Canvas(viz_frame, width=500, height=400)
        self.canvas.grid(row=0, column=0)

    def allocate_resource(self):
        """ Allocates a resource to a process and updates the visualization dynamically """
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()
        if process and resource:
            message = self.manager.allocate(process, resource)
            print(message)
            self.process_entry.delete(0, tk.END)
            self.resource_entry.delete(0, tk.END)
            self.visualizer.show_graph()  # Auto-update graph

    def release_resource(self):
        """ Releases a resource from a process and updates the visualization dynamically """
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()
        if process and resource:
            message = self.manager.release(process, resource)
            print(message)
            self.process_entry.delete(0, tk.END)
            self.resource_entry.delete(0, tk.END)
            self.visualizer.show_graph()  # Auto-update graph

    def check_deadlock(self):
        has_deadlock, message = self.manager.detect_deadlock()
        print(message)
        if has_deadlock:
            messagebox.showwarning("Deadlock Alert", message)
        else:
            messagebox.showinfo("Deadlock Check", message)

    def clear_log(self):
        message = self.manager.clear_all()
        print(message)
        self.visualizer.show_graph()  # Auto-update graph after clearing

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ResourceAllocationApp()
    app.run()
