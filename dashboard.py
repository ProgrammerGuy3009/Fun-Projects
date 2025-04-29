import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import csv
import datetime
import requests
import threading
import time
import json
import os

class H1N1Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("H1N1 Influenza Dashboard - Seasonal Analysis")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set theme color
        self.primary_color = "#2e86de"
        self.secondary_color = "#f5f6fa"
        self.accent_color = "#ff6b6b"
        self.text_color = "#2f3542"
        
        # Configure root window style
        self.root.configure(bg=self.secondary_color)
        
        # Create styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.secondary_color)
        self.style.configure('TButton', background=self.primary_color, foreground='white')
        self.style.configure('TLabel', background=self.secondary_color, foreground=self.text_color)
        self.style.configure('TNotebook', background=self.secondary_color)
        self.style.configure('TNotebook.Tab', background=self.secondary_color, padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', self.primary_color)], foreground=[('selected', 'white')])
        
        # Initialize data
        self.data = None
        self.states = []
        self.years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
        self.metrics = ['Cases', 'Deaths']
        
        # Simulated real-time data timestamp
        self.last_update = datetime.datetime.now()
        self.auto_refresh = False
        self.refresh_thread = None
        self.kill_thread = False
        
        # Loading data
        self.load_data()
        
        # Create main layout
        self.create_gui()
        
        # Start real-time simulation if enabled
        self.start_real_time_simulation()
    
    def load_data(self):
        """Load data from CSV file"""
        try:
            # Check if file exists, otherwise create default data
            if os.path.exists('h1n1_data.csv'):
                self.data = pd.read_csv('h1n1_data.csv')
            else:
                # Create CSV data
                data_str = """State_UT,2019_Cases,2019_Deaths,2020_Cases,2020_Deaths,2021_Cases,2021_Deaths,2022_Cases,2022_Deaths,2023_Cases,2023_Deaths,2024_Cases,2024_Deaths,2025_Cases,2025_Deaths
Andaman & Nicobar,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Andhra Pradesh,333,15,33,2,1,0,22,0,103,0,125,0,5,0
Arunachal Pradesh,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Assam,57,2,4,0,0,0,63,0,2,0,28,3,0,0
Bihar,52,1,17,0,0,0,0,0,0,0,0,0,0,0
Chandigarh,54,3,17,3,0,0,21,0,10,0,24,0,1,0
Chhattisgarh,169,28,10,1,6,1,399,4,35,9,622,43,1,0
Dadra & Nagar Haveli,7,3,1,0,0,0,0,0,0,0,13,0,0,0
Daman & Diu,9,1,0,0,0,0,0,0,0,0,3,0,0,0
Delhi,3627,31,412,0,92,0,442,0,209,0,3151,0,40,0
Goa,108,3,1,0,6,0,217,0,105,0,103,0,5,0
Gujarat,4844,151,55,2,33,2,2174,71,212,3,1711,55,14,0
Haryana,1041,16,44,0,6,0,103,12,30,4,307,26,3,0
Himachal Pradesh,335,41,31,1,0,0,8,1,19,1,68,3,4,1
Jammu & Kashmir,447,27,106,0,4,0,69,3,39,0,130,1,41,0
Jharkhand,80,5,2,0,0,0,34,0,1,0,18,1,1,0
Karnataka,2030,96,458,3,13,0,517,15,118,0,3530,10,76,1
Kerala,845,44,71,2,0,0,90,7,1025,57,2846,61,48,4
Lakshadweep,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Madhya Pradesh,720,165,20,1,2,1,53,2,0,0,157,1,2,0
Maharashtra,2287,246,121,3,387,2,3714,215,1231,32,2072,71,21,0
Manipur,3,1,4,0,0,0,3,0,1,0,1,0,0,0
Meghalaya,2,0,1,0,1,0,2,0,4,0,28,0,0,0
Mizoram,0,0,0,0,0,0,0,0,17,0,120,0,0,0
Nagaland,0,0,0,0,0,0,0,0,0,0,20,0,0,0
Odisha,206,5,35,1,0,0,142,0,42,0,30,0,0,0
Puducherry,29,0,7,0,52,0,296,0,269,0,207,0,32,0
Punjab,541,31,68,5,3,0,203,42,93,4,356,48,4,0
Rajasthan,5092,208,116,1,20,1,365,11,127,0,1149,12,0,0
Sikkim,8,0,1,0,0,0,48,0,28,0,150,0,0,0
Tamil Nadu,1038,4,276,1,11,0,2827,25,3544,19,1777,4,209,0
Telangana,1388,22,446,5,9,0,343,0,165,0,104,0,3,0
Tripura,31,0,0,0,0,0,0,0,0,0,77,0,1,0
Uttarakhand,246,6,13,1,0,0,0,0,17,0,270,1,2,0
Uttar Pradesh,2096,37,252,12,24,1,388,2,123,0,205,5,0,0
West Bengal,1073,26,130,0,108,4,659,0,556,0,1012,2,3,0
Total,28798,1218,2752,44,778,12,13202,410,8125,129,20414,347,516,6"""
                
                with open('h1n1_data.csv', 'w', newline='') as f:
                    f.write(data_str)
                    
                self.data = pd.read_csv('h1n1_data.csv')
            
            self.states = self.data['State_UT'].tolist()
            
            # Create summary statistics
            self.total_cases_by_year = {}
            self.total_deaths_by_year = {}
            
            for year in self.years:
                self.total_cases_by_year[year] = self.data[f'{year}_Cases'].sum()
                self.total_deaths_by_year[year] = self.data[f'{year}_Deaths'].sum()
                
        except Exception as e:
            messagebox.showerror("Data Loading Error", f"Error loading data: {str(e)}")
    
    def create_gui(self):
        """Create the main GUI elements"""
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header with title and controls
        self.create_header()
        
        # Create tabs for different views
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create dashboard tab
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.create_dashboard()
        
        # Create comparative analysis tab
        self.comparative_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.comparative_tab, text="Comparative Analysis")
        self.create_comparative_analysis()
        
        # Create state-wise analysis tab
        self.state_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.state_tab, text="State-wise Analysis")
        self.create_state_analysis()
        
        # Create timeline analysis tab
        self.timeline_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.timeline_tab, text="Timeline Analysis")
        self.create_timeline_analysis()
        
        # Create data table tab
        self.data_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.data_tab, text="Data Table")
        self.create_data_table()
        
        # Create status bar
        self.status_bar = ttk.Frame(self.main_frame, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
        self.status_label = ttk.Label(self.status_bar, text=f"Last updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.auto_refresh_var = tk.BooleanVar(value=False)
        self.auto_refresh_check = ttk.Checkbutton(self.status_bar, text="Auto refresh (simulating real-time data)", 
                                               variable=self.auto_refresh_var, command=self.toggle_auto_refresh)
        self.auto_refresh_check.pack(side=tk.RIGHT, padx=5)
    
    def create_header(self):
        """Create header with title and controls"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Seasonal Influenza A (H1N1) Dashboard", 
                               font=("Arial", 16, "bold"), foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Controls
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        refresh_btn = ttk.Button(controls_frame, text="Refresh Data", command=self.refresh_data)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(controls_frame, text="Export Data", command=self.export_data)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        about_btn = ttk.Button(controls_frame, text="About", command=self.show_about)
        about_btn.pack(side=tk.LEFT, padx=5)
    
    def create_dashboard(self):
        """Create main dashboard with summary graphs"""
        # Create top frame for key metrics
        metrics_frame = ttk.Frame(self.dashboard_tab)
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add key metrics
        total_cases = sum(self.total_cases_by_year.values())
        total_deaths = sum(self.total_deaths_by_year.values())
        mortality_rate = (total_deaths / total_cases) * 100 if total_cases > 0 else 0
        latest_year_cases = self.total_cases_by_year['2025']
        
        self.create_metric_box(metrics_frame, "Total Cases", f"{total_cases:,}", "blue")
        self.create_metric_box(metrics_frame, "Total Deaths", f"{total_deaths:,}", "red")
        self.create_metric_box(metrics_frame, "Mortality Rate", f"{mortality_rate:.2f}%", "orange")
        self.create_metric_box(metrics_frame, "2025 Cases (YTD)", f"{latest_year_cases:,}", "green")
        
        # Create bottom frame for graphs
        graphs_frame = ttk.Frame(self.dashboard_tab)
        graphs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Split into two columns
        left_frame = ttk.Frame(graphs_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(graphs_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Add charts
        self.create_yearly_trend_chart(left_frame)
        self.create_top_states_chart(right_frame)
        self.create_mortality_rate_chart(left_frame)
        self.create_cases_vs_deaths_chart(right_frame)
        self.create_seasonal_chart(graphs_frame)
    
    def create_metric_box(self, parent, title, value, color):
        """Create a metric box for the dashboard"""
        frame = ttk.Frame(parent, borderwidth=1, relief=tk.RAISED)
        frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        title_label = ttk.Label(frame, text=title, font=("Arial", 10))
        title_label.pack(anchor=tk.CENTER, pady=(5, 0))
        
        value_label = ttk.Label(frame, text=value, font=("Arial", 16, "bold"), foreground=color)
        value_label.pack(anchor=tk.CENTER, pady=(0, 5))
    
    def create_yearly_trend_chart(self, parent):
        """Create yearly trend chart"""
        frame = ttk.LabelFrame(parent, text="Yearly Trend of H1N1 Cases")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(5, 3))
        years = list(self.total_cases_by_year.keys())
        cases = list(self.total_cases_by_year.values())
        
        ax.bar(years, cases, color=self.primary_color)
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Cases')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.yearly_trend_chart = {"fig": fig, "ax": ax, "canvas": canvas}
    
    def create_top_states_chart(self, parent):
        """Create top states chart"""
        frame = ttk.LabelFrame(parent, text="Top 10 States by H1N1 Cases (All Years)")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Calculate total cases by state
        total_cases_by_state = {}
        for state in self.states:
            if state == "Total":
                continue
            state_cases = 0
            for year in self.years:
                col_name = f'{year}_Cases'
                state_cases += self.data.loc[self.data['State_UT'] == state, col_name].values[0]
            total_cases_by_state[state] = state_cases
        
        # Sort and get top 10
        sorted_states = sorted(total_cases_by_state.items(), key=lambda x: x[1], reverse=True)[:10]
        top_states = [s[0] for s in sorted_states]
        top_values = [s[1] for s in sorted_states]
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(5, 3))
        y_pos = np.arange(len(top_states))
        
        ax.barh(y_pos, top_values, color=self.accent_color)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_states)
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('Number of Cases')
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.top_states_chart = {"fig": fig, "ax": ax, "canvas": canvas}
    
    def create_mortality_rate_chart(self, parent):
        """Create mortality rate chart"""
        frame = ttk.LabelFrame(parent, text="Yearly Mortality Rate")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Calculate mortality rate by year
        mortality_rates = []
        for year in self.years:
            cases = self.total_cases_by_year[year]
            deaths = self.total_deaths_by_year[year]
            rate = (deaths / cases) * 100 if cases > 0 else 0
            mortality_rates.append(rate)
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(self.years, mortality_rates, marker='o', color='red', linewidth=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Mortality Rate (%)')
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout(rect=[0, 0, 1, 0.9])  # Leave more space at the top for the legend
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.mortality_chart = {"fig": fig, "ax": ax, "canvas": canvas}
    
    def create_cases_vs_deaths_chart(self, parent):
        """Create cases vs deaths chart"""
        frame = ttk.LabelFrame(parent, text="Cases vs Deaths by Year")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Prepare data
        years = list(self.total_cases_by_year.keys())
        cases = list(self.total_cases_by_year.values())
        deaths = list(self.total_deaths_by_year.values())
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(5, 3))
        
        x = np.arange(len(years))
        width = 0.35
        
        rects1 = ax.bar(x - width/2, cases, width, label='Cases', color=self.primary_color)
        ax2 = ax.twinx()
        rects2 = ax2.bar(x + width/2, deaths, width, label='Deaths', color='red')
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Cases')
        ax2.set_ylabel('Number of Deaths')
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.tick_params(axis='x', rotation=90)
        
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.15), 
          ncol=2, frameon=False)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.cases_deaths_chart = {"fig": fig, "ax": ax, "ax2": ax2, "canvas": canvas}
    
    def create_seasonal_chart(self, parent):
        """Create seasonal analysis chart"""
        frame = ttk.LabelFrame(parent, text="Geographic Distribution (2024)")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Filter data for the most recent complete year
        recent_year = '2024'
        
        # Get top 10 states by cases for the most recent year
        cases_col = f'{recent_year}_Cases'
        state_data = self.data[self.data['State_UT'] != 'Total'].sort_values(by=cases_col, ascending=False).head(10)
        
        states = state_data['State_UT'].tolist()
        cases = state_data[cases_col].tolist()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(6, 4))
        explode = [0.1 if i == 0 else 0 for i in range(len(states))]
        
        # ax.pie(cases, explode=explode, labels=states, autopct='%1.1f%%',
        #       shadow=True, startangle=90, textprops={'fontsize': 8})
        wedges, texts, autotexts = ax.pie(cases, explode=explode, labels=None, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
        # Add legend instead of direct labels
        ax.legend(wedges, states, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.seasonal_chart = {"fig": fig, "ax": ax, "canvas": canvas}
    
    def create_comparative_analysis(self):
        """Create comparative analysis tab"""
        # Top control frame
        control_frame = ttk.Frame(self.comparative_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # State selection
        ttk.Label(control_frame, text="Select States:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.state_selections = []
        self.state_vars = []
        
        # Create a scrollable frame for state checkboxes
        state_frame = ttk.Frame(control_frame)
        state_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Get the top 10 states by total cases
        total_cases_by_state = {}
        for state in self.states:
            if state == "Total":
                continue
            state_cases = 0
            for year in self.years:
                col_name = f'{year}_Cases'
                state_cases += self.data.loc[self.data['State_UT'] == state, col_name].values[0]
            total_cases_by_state[state] = state_cases
        
        top_states = sorted(total_cases_by_state.items(), key=lambda x: x[1], reverse=True)[:10]
        top_state_names = [s[0] for s in top_states]
        
        # Add top 5 states as default selections
        for i, state in enumerate(top_state_names[:5]):
            var = tk.BooleanVar(value=True)
            self.state_vars.append(var)
            cb = ttk.Checkbutton(state_frame, text=state, variable=var)
            cb.pack(side=tk.LEFT, padx=5)
            self.state_selections.append((state, cb, var))
        
        # Metric selection
        ttk.Label(control_frame, text="Metric:").pack(side=tk.LEFT, padx=(20, 5))
        self.metric_var = tk.StringVar(value="Cases")
        metric_cb = ttk.Combobox(control_frame, textvariable=self.metric_var, values=["Cases", "Deaths"])
        metric_cb.pack(side=tk.LEFT, padx=5)
        metric_cb.config(state="readonly")
        
        # Year range
        ttk.Label(control_frame, text="Year Range:").pack(side=tk.LEFT, padx=(20, 5))
        self.start_year_var = tk.StringVar(value="2019")
        start_year_cb = ttk.Combobox(control_frame, textvariable=self.start_year_var, values=self.years)
        start_year_cb.pack(side=tk.LEFT, padx=5)
        start_year_cb.config(state="readonly", width=5)
        
        ttk.Label(control_frame, text="to").pack(side=tk.LEFT)
        
        self.end_year_var = tk.StringVar(value="2025")
        end_year_cb = ttk.Combobox(control_frame, textvariable=self.end_year_var, values=self.years)
        end_year_cb.pack(side=tk.LEFT, padx=5)
        end_year_cb.config(state="readonly", width=5)
        
        # Update button
        update_btn = ttk.Button(control_frame, text="Update", command=self.update_comparative_chart)
        update_btn.pack(side=tk.LEFT, padx=(20, 5))
        
        # Chart frame
        chart_frame = ttk.Frame(self.comparative_tab)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create initial comparative chart
        self.create_comparative_chart(chart_frame)
    
    def create_comparative_chart(self, parent):
        """Create comparative analysis chart"""
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get selected states
        selected_states = []
        for state, _, var in self.state_selections:
            if var.get():
                selected_states.append(state)
        
        if not selected_states:
            selected_states = [self.state_selections[0][0]]  # Default to first state if none selected
        
        # Get selected metric and years
        metric = self.metric_var.get()
        start_year = self.start_year_var.get()
        end_year = self.end_year_var.get()
        
        # Get indices for year range
        start_idx = self.years.index(start_year)
        end_idx = self.years.index(end_year)
        year_range = self.years[start_idx:end_idx+1]
        
        # Plot data for each selected state
        for state in selected_states:
            values = []
            for year in year_range:
                col_name = f'{year}_{metric}'
                value = self.data.loc[self.data['State_UT'] == state, col_name].values[0]
                values.append(value)
            
            ax.plot(year_range, values, marker='o', linewidth=2, label=state)
        
        ax.set_xlabel('Year')
        ax.set_ylabel(f'Number of {metric}')
        ax.set_title(f'Comparative Analysis of {metric} by State (Year: {start_year}-{end_year})')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        fig.tight_layout()
        
        # Clear existing canvas if it exists
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store for later reference
        self.comparative_chart = {"fig": fig, "ax": ax, "canvas": canvas}
    
    def update_comparative_chart(self):
        """Update the comparative chart based on selections"""
        if hasattr(self, 'comparative_chart'):
            chart_frame = self.comparative_chart["canvas"].get_tk_widget().master
            self.create_comparative_chart(chart_frame)
    
    def create_state_analysis(self):
        """Create state-wise analysis tab"""
        # Top control frame
        control_frame = ttk.Frame(self.state_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # State selection
        ttk.Label(control_frame, text="Select State:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.selected_state_var = tk.StringVar(value="Tamil Nadu")
        state_cb = ttk.Combobox(control_frame, textvariable=self.selected_state_var, 
                               values=[s for s in self.states if s != "Total"])
        state_cb.pack(side=tk.LEFT, padx=5)
        state_cb.config(state="readonly")
        
        # Year selection
        ttk.Label(control_frame, text="Year:").pack(side=tk.LEFT, padx=(20, 5))
        self.selected_year_var = tk.StringVar(value="2024")
        year_cb = ttk.Combobox(control_frame, textvariable=self.selected_year_var, values=self.years)
        year_cb.pack(side=tk.LEFT, padx=5)
        year_cb.config(state="readonly")
        
        # Update button
        update_btn = ttk.Button(control_frame, text="Generate Analysis", command=self.update_state_analysis)
        update_btn.pack(side=tk.LEFT, padx=(20, 5))
        
        # Content frame - split into info and chart
        content_frame = ttk.Frame(self.state_tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info panel
        self.state_info_frame = ttk.LabelFrame(content_frame, text="State Information")
        self.state_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Chart panel
        self.state_chart_frame = ttk.LabelFrame(content_frame, text="State Trend Analysis")
        self.state_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create initial state analysis
        self.update_state_analysis()
    
    def update_state_analysis(self):
        """Update the state analysis based on selections"""
        # Clear existing content
        for widget in self.state_info_frame.winfo_children():
            widget.destroy()
        
        for widget in self.state_chart_frame.winfo_children():
            widget.destroy()
        
        state = self.selected_state_var.get()
        
        # Information panel
        info_text = ScrolledText(self.state_info_frame, wrap=tk.WORD, width=40, height=20)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get state data
        state_data = {}
        for year in self.years:
            cases = self.data.loc[self.data['State_UT'] == state, f'{year}_Cases'].values[0]
            deaths = self.data.loc[self.data['State_UT'] == state, f'{year}_Deaths'].values[0]
            mortality = (deaths / cases) * 100 if cases > 0 else 0
            state_data[year] = {'cases': cases, 'deaths': deaths, 'mortality': mortality}
        
        # Calculate rankings
        all_states_data = {}
        for s in self.states:
            if s == "Total":
                continue
            all_states_data[s] = sum(self.data.loc[self.data['State_UT'] == s, [f'{y}_Cases' for y in self.years]].values[0])
        
        sorted_states = sorted(all_states_data.items(), key=lambda x: x[1], reverse=True)
        rank = next((i + 1 for i, (s, _) in enumerate(sorted_states) if s == state), "N/A")
        
        # Prepare text
        total_cases = sum(data['cases'] for data in state_data.values())
        total_deaths = sum(data['deaths'] for data in state_data.values())
        avg_mortality = (total_deaths / total_cases) * 100 if total_cases > 0 else 0
        
        current_year_data = state_data[self.selected_year_var.get()]
        
        info_text.insert(tk.END, f"State: {state}\n\n")
        info_text.insert(tk.END, f"Overall Rank: {rank} out of {len(all_states_data)} states/UTs\n\n")
        info_text.insert(tk.END, f"Total Cases (2019-2025): {total_cases:,}\n")
        info_text.insert(tk.END, f"Total Deaths (2019-2025): {total_deaths:,}\n")
        info_text.insert(tk.END, f"Overall Mortality Rate: {avg_mortality:.2f}%\n\n")
        
        info_text.insert(tk.END, f"Selected Year ({self.selected_year_var.get()}) Statistics:\n")
        info_text.insert(tk.END, f"  - Cases: {current_year_data['cases']:,}\n")
        info_text.insert(tk.END, f"  - Deaths: {current_year_data['deaths']:,}\n")
        info_text.insert(tk.END, f"  - Mortality Rate: {current_year_data['mortality']:.2f}%\n\n")
        
        info_text.insert(tk.END, "Year-wise Data:\n")
        for year in self.years:
            info_text.insert(tk.END, f"  - {year}: {state_data[year]['cases']:,} cases, {state_data[year]['deaths']:,} deaths\n")
        
        info_text.configure(state='disabled')
        
        # Chart - create trend analysis
        fig, ax = plt.subplots(figsize=(6, 8))
        
        years = list(state_data.keys())
        cases = [state_data[y]['cases'] for y in years]
        deaths = [state_data[y]['deaths'] for y in years]
        
        # Twin axis plot
        ax.bar(years, cases, color=self.primary_color, alpha=0.7, label='Cases')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Cases', color=self.primary_color)
        ax.tick_params(axis='y', labelcolor=self.primary_color)
        ax.tick_params(axis='x', rotation=90)
        
        ax2 = ax.twinx()
        ax2.plot(years, deaths, color='red', marker='o', linewidth=2, label='Deaths')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        
        fig.tight_layout()
        
        # Add a combined legend
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc='upper left')
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.state_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_timeline_analysis(self):
        """Create timeline analysis tab"""
        # Top frame for controls
        control_frame = ttk.Frame(self.timeline_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Metric selection
        ttk.Label(control_frame, text="Select Metric:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.timeline_metric_var = tk.StringVar(value="Cases")
        metric_rb1 = ttk.Radiobutton(control_frame, text="Cases", variable=self.timeline_metric_var, value="Cases")
        metric_rb1.pack(side=tk.LEFT, padx=5)
        
        metric_rb2 = ttk.Radiobutton(control_frame, text="Deaths", variable=self.timeline_metric_var, value="Deaths")
        metric_rb2.pack(side=tk.LEFT, padx=5)
        
        metric_rb3 = ttk.Radiobutton(control_frame, text="Mortality Rate", variable=self.timeline_metric_var, value="Mortality")
        metric_rb3.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_btn = ttk.Button(control_frame, text="Update Timeline", command=self.update_timeline)
        update_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create charts frame
        charts_frame = ttk.Frame(self.timeline_tab)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create timeline chart - one big one
        self.timeline_chart_frame = ttk.Frame(charts_frame)
        self.timeline_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create initial timeline
        self.create_timeline_chart()
    
    def create_timeline_chart(self):
        """Create timeline chart"""
        # Clear existing widgets
        for widget in self.timeline_chart_frame.winfo_children():
            widget.destroy()
        
        metric = self.timeline_metric_var.get()
        
        if metric == "Cases":
            data_by_year = self.total_cases_by_year
            color = self.primary_color
            title = "Timeline of H1N1 Cases (2019-2025)"
            ylabel = "Number of Cases"
        elif metric == "Deaths":
            data_by_year = self.total_deaths_by_year
            color = "red"
            title = "Timeline of H1N1 Deaths (2019-2025)"
            ylabel = "Number of Deaths"
        else:  # Mortality
            data_by_year = {}
            for year in self.years:
                cases = self.total_cases_by_year[year]
                deaths = self.total_deaths_by_year[year]
                data_by_year[year] = (deaths / cases) * 100 if cases > 0 else 0
            color = "orange"
            title = "Timeline of H1N1 Mortality Rate (2019-2025)"
            ylabel = "Mortality Rate (%)"
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        years = list(data_by_year.keys())
        values = list(data_by_year.values())
        
        # Line plot with markers and area fill
        ax.plot(years, values, marker='o', markersize=8, linewidth=2, color=color)
        ax.fill_between(years, values, alpha=0.3, color=color)
        
        # Add data labels
        for i, (year, value) in enumerate(zip(years, values)):
            if metric == "Mortality":
                ax.annotate(f"{value:.2f}%", (year, value), 
                         textcoords="offset points", xytext=(0, 10), ha='center')
            else:
                ax.annotate(f"{int(value):,}", (year, value), 
                         textcoords="offset points", xytext=(0, 10), ha='center')
        
        # Set chart properties
        ax.set_xlabel('Year')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add trend line
        z = np.polyfit(range(len(years)), values, 1)
        p = np.poly1d(z)
        ax.plot(years, p(range(len(years))), "r--", alpha=0.7)
        
        fig.tight_layout()
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.timeline_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_timeline(self):
        """Update timeline chart"""
        self.create_timeline_chart()
    
    def create_data_table(self):
        """Create data table tab"""
        # Top frame for controls
        control_frame = ttk.Frame(self.data_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search function
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = ttk.Button(control_frame, text="Search", command=self.filter_table)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(control_frame, text="Clear", command=self.clear_filter)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = ttk.Button(control_frame, text="Export CSV", command=self.export_table_data)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(self.data_tab)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview with scrollbars
        self.tree = ttk.Treeview(table_frame)
        
        # Add vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Pack the treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Define columns
        columns = ['State_UT']
        for year in self.years:
            columns.extend([f'{year}_Cases', f'{year}_Deaths'])
        
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Define headings
        for col in columns:
            if col == 'State_UT':
                self.tree.heading(col, text="State/UT")
                self.tree.column(col, width=150, anchor=tk.W)
            else:
                year, metric = col.split('_')
                self.tree.heading(col, text=f"{year} {metric}")
                self.tree.column(col, width=80, anchor=tk.E)
        
        # Insert data
        self.populate_table()
    
    def populate_table(self, filtered_data=None):
        """Populate the data table"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Use filtered data if provided, otherwise use all data
        data_to_show = filtered_data if filtered_data is not None else self.data
        
        # Insert data
        for index, row in data_to_show.iterrows():
            values = [row['State_UT']]
            for year in self.years:
                values.extend([int(row[f'{year}_Cases']), int(row[f'{year}_Deaths'])])
            
            self.tree.insert("", tk.END, values=values)
    
    def filter_table(self):
        """Filter the data table based on search term"""
        search_term = self.search_var.get().lower()
        if search_term:
            filtered_data = self.data[self.data['State_UT'].str.lower().str.contains(search_term)]
            self.populate_table(filtered_data)
        else:
            self.populate_table()
    
    def clear_filter(self):
        """Clear the search filter"""
        self.search_var.set("")
        self.populate_table()
    
    def export_table_data(self):
        """Export the table data to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Data to CSV"
        )
        
        if file_path:
            try:
                self.data.to_csv(file_path, index=False)
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
    
    def refresh_data(self):
        """Refresh all data"""
        # Simulate data refresh
        self.last_update = datetime.datetime.now()
        self.status_label.config(text=f"Last updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Add slight random variations to 2025 data to simulate real-time updates
        if self.data is not None:
            # Only modify the 2025 data
            for index, row in self.data.iterrows():
                state = row['State_UT']
                if state != 'Total' and row['2025_Cases'] > 0:
                    # Add small random change
                    change = np.random.randint(-2, 5)
                    new_value = max(0, row['2025_Cases'] + change)
                    self.data.at[index, '2025_Cases'] = new_value
            
            # Update the total row
            total_cases = self.data[self.data['State_UT'] != 'Total']['2025_Cases'].sum()
            total_index = self.data[self.data['State_UT'] == 'Total'].index[0]
            self.data.at[total_index, '2025_Cases'] = total_cases
            
            # Update summary statistics
            self.total_cases_by_year['2025'] = total_cases
        
        # Update all visualizations
        self.update_all_charts()
        
        # Show success message
        messagebox.showinfo("Data Refreshed", "Dashboard data has been refreshed successfully.")
    
    def update_all_charts(self):
        """Update all charts with new data"""
        # Update dashboard charts
        if hasattr(self, 'yearly_trend_chart'):
            self.yearly_trend_chart["ax"].clear()
            years = list(self.total_cases_by_year.keys())
            cases = list(self.total_cases_by_year.values())
            self.yearly_trend_chart["ax"].bar(years, cases, color=self.primary_color)
            self.yearly_trend_chart["ax"].set_xlabel('Year')
            self.yearly_trend_chart["ax"].set_ylabel('Number of Cases')
            self.yearly_trend_chart["ax"].tick_params(axis='x', rotation=45)
            self.yearly_trend_chart["ax"].grid(axis='y', linestyle='--', alpha=0.7)
            self.yearly_trend_chart["fig"].tight_layout()
            self.yearly_trend_chart["canvas"].draw()
        
        # Update other tabs
        if hasattr(self, 'comparative_chart'):
            self.update_comparative_chart()
        
        if hasattr(self, 'state_info_frame'):
            self.update_state_analysis()
        
        if hasattr(self, 'timeline_chart_frame'):
            self.create_timeline_chart()
        
        # Update data table
        if hasattr(self, 'tree'):
            self.populate_table()
    
    def toggle_auto_refresh(self):
        """Toggle auto refresh functionality"""
        self.auto_refresh = self.auto_refresh_var.get()
        
        if self.auto_refresh:
            self.start_real_time_simulation()
        else:
            self.kill_thread = True
    
    def start_real_time_simulation(self):
        """Start thread for real-time data simulation"""
        if self.auto_refresh and not self.refresh_thread:
            self.kill_thread = False
            self.refresh_thread = threading.Thread(target=self.auto_refresh_data)
            self.refresh_thread.daemon = True
            self.refresh_thread.start()
    
    def auto_refresh_data(self):
        """Auto refresh data periodically"""
        while not self.kill_thread:
            time.sleep(30)  # Refresh every 30 seconds
            
            if self.kill_thread:
                break
                
            # Use after to update UI from main thread
            self.root.after(0, self.refresh_data)
        
        self.refresh_thread = None
    
    def export_data(self):
        """Export data to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Data to CSV"
        )
        
        if file_path:
            try:
                self.data.to_csv(file_path, index=False)
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        H1N1 Influenza Dashboard
        
        Version: 1.0
        
        A comprehensive dashboard for analyzing Seasonal Influenza A (H1N1) 
        data across different states in India from 2019 to 2025.
        
        Features:
        - Interactive visualizations
        - State-wise analysis
        - Comparative trend analysis
        - Data table with export functionality
        - Real-time data simulation
        
        Created for the DVA Project Assignment.
        """
        
        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = H1N1Dashboard(root)
    root.mainloop()