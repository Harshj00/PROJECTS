import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

class HousePricePredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("K.R.M.U Property Price Predictor")
        
        # Make window responsive
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Make window resizable
        self.root.resizable(True, True)
        
        self.root.configure(bg='#1a1a2e')  # Dark modern background
        
        # Enable high FPS animations
        self.root.tk.call('tk', 'scaling', 1.9)
        self.root.update_idletasks()
        
        # Modern style configuration
        self.style = {
            'bg_primary': '#41038f',        # light face colour
            'bg_secondary': '#d4fff7',
            'accent': '#64FFDA',            # Mint green
            'accent_light': '#7c7e80',      # Bright mint
            'text_primary': '#030000',      # Bright white-blue
            'text_secondary': '#050b14',    # Muted blue-gray
            'highlight': '#FF6B6B',         # Coral red
            'success': '#00FFFF',           # Cyan blue
            'input_bg': '#dddec8',          # Deep blue for inputs
            'gradient_start': '#0A192F',    # Gradient dark
            'gradient_end': '#112240',      # Gradient light
            'border': '#050b14',            # Border color
            'label_text': '#2d2d3a'         # New darker matte color for labels
        }

        # Initialize the scaler and model
        self.initialize_model()

        # Enhanced feature set
        self.features = {
            'Square_Footage': tk.StringVar(),
            'Bedrooms': tk.StringVar(),
            'Bathrooms': tk.StringVar(),
            'Location_Rating': tk.StringVar(),
            'Floor_Number': tk.StringVar(),
            'Parking_Spots': tk.StringVar(),
            'Swimming_Pool': tk.StringVar(),
            'Security_Rating': tk.StringVar()
        }

        # Load and set background image
        try:
            bg_image = Image.open("background.jpg")
            bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(root, image=self.bg_photo)  # type: ignore
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Using gradient background: {e}")
            self.root.configure(bg=self.style['bg_primary'])

        # Create main scrollable container with modern look
        self.main_canvas = tk.Canvas(
            root,
            bg=self.style['bg_primary'],
            highlightthickness=0,
            bd=0
        )
        
        # Modern scrollbar style
        scrollbar = ttk.Scrollbar(
            root,
            orient="vertical",
            command=self.main_canvas.yview,
            style="Modern.Vertical.TScrollbar"
        )
        
        # Configure ttk styles
        self.configure_styles()
        
        # Add smooth scrolling
        self.main_canvas.configure(yscrollcommand=self.smooth_scroll)
        
        self.scrollable_frame = tk.Frame(self.main_canvas)
        
        # Configure scrollable frame
        self.scrollable_frame.configure(bg=self.style['bg_primary'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack main containers
        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create main container
        self.main_container = tk.Frame(
            self.scrollable_frame,
            bg=self.style['bg_primary']
        )
        self.main_container.pack(expand=True, fill='both', padx=30, pady=30)

        # Initialize result frame and labels
        self.fancy_result_frame = tk.Frame(
            self.main_container,
            bg=self.style['bg_secondary'],
            bd=2,
            relief='raised'
        )
        self.fancy_result_frame.pack(fill='x', pady=20, padx=10)

        self.result_title = tk.Label(
            self.fancy_result_frame,
            text="Property Valuation",
            font=("Helvetica", 16, "bold"),
            bg=self.style['bg_secondary'],
            fg=self.style['text_primary']
        )
        self.result_title.pack(pady=10)

        self.result_label = tk.Label(
            self.fancy_result_frame,
            text="Enter property details and click Calculate",
            font=("Helvetica", 14),
            bg=self.style['bg_secondary'],
            fg=self.style['text_primary']
        )
        self.result_label.pack(pady=10)

        # Create sections
        self.create_glass_effect_header()
        self.create_glass_effect_content()
        self.create_prediction_section()

        # Bind mousewheel
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def configure_styles(self):
        # Configure ttk styles for modern look
        style = ttk.Style()
        
        # Configure scrollbar
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=self.style['bg_secondary'],
            troughcolor=self.style['bg_primary'],
            width=10,
            arrowsize=0
        )
        
        # Configure entry fields
        style.configure(
            "Modern.TEntry",
            fieldbackground=self.style['bg_secondary'],
            foreground=self.style['text_primary'],
            padding=10
        )

    def create_glass_effect_header(self):
        header_frame = tk.Frame(
            self.main_container,
            bg=self.style['bg_primary'],
            bd=0
        )
        header_frame.pack(fill='x', pady=(0, 20))

        # Animated gradient header
        self.header_label = tk.Label(
            header_frame,
            text="✨ Premium Property Valuation ✨",
            font=("Helvetica", 36, "bold"),
            fg=self.style['accent'],
            bg=self.style['bg_primary']
        )
        self.header_label.pack(pady=20)
        self.animate_header()

    def animate_header(self):
        colors = [self.style['accent'], self.style['accent_light']]
        current_color = 0
        
        def update_color():
            nonlocal current_color
            self.header_label.configure(fg=colors[current_color])
            current_color = (current_color + 1) % 2
            self.root.after(1000, update_color)
        
        update_color()

    def create_glass_effect_content(self):
        content_frame = tk.Frame(
            self.main_container,
            bg=self.style['bg_secondary'],
            bd=2,
            relief='raised'
        )
        content_frame.pack(fill='both', expand=True, pady=10)

        # Add decorative line at the top
        separator = tk.Frame(content_frame, height=2, bg=self.style['accent'])
        separator.pack(fill='x', pady=(0, 10))

        # Create grid container
        grid_frame = tk.Frame(content_frame, bg=self.style['bg_secondary'])
        grid_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Configure grid columns
        for i in range(4):
            grid_frame.columnconfigure(i, weight=1, pad=10)

        # Update the labels in create_glass_effect_content method
        label_texts = {
            'Square_Footage': 'Square Footage (sq ft)',
            'Location_Rating': 'Location Rating (1-10)',
            'Security_Rating': 'Security Rating (1-10)',
            'Swimming_Pool': 'Swimming Pool (0/1)',
        }

        # Create input fields in grid layout
        row, col = 0, 0
        for feature, var in self.features.items():
            # Create frame for each input
            frame = tk.Frame(grid_frame, bg=self.style['bg_secondary'])
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Label with icon
            icon = self.get_feature_icon(feature)
            label_text = f"{icon} {label_texts.get(feature, feature)}"
            
            label = tk.Label(
                frame,
                text=label_text,
                font=("Helvetica", 11, "bold"),
                fg=self.style['label_text'],
                bg=self.style['bg_secondary'],
                wraplength=150  # Wrap long text
            )
            label.pack(anchor='w', pady=(0, 5))
            
            # Styled entry with glowing effect
            entry_frame = tk.Frame(frame, bg=self.style['border'], bd=1, relief='solid')
            entry_frame.pack(fill='x')
            
            entry = tk.Entry(
                entry_frame,
                textvariable=var,
                font=("Helvetica", 11),
                bg=self.style['input_bg'],
                fg=self.style['text_primary'],
                insertbackground=self.style['accent'],
                relief='flat',
                width=20
            )
            entry.pack(fill='x', padx=1, pady=1)

            # Add hover effect
            def on_enter(e, ef=entry_frame):
                ef.configure(bg=self.style['accent'])
            def on_leave(e, ef=entry_frame):
                ef.configure(bg=self.style['border'])
                
            entry_frame.bind("<Enter>", on_enter)
            entry_frame.bind("<Leave>", on_leave)

            # Update grid position
            col += 1
            if col >= 4:  # Move to next row after 4 columns
                col = 0
                row += 1

    def create_prediction_section(self):
        prediction_frame = tk.Frame(
            self.main_container,
            bg=self.style['bg_secondary'],
            bd=2,
            relief='raised'
        )
        prediction_frame.pack(fill='x', pady=20, padx=10)

        # Button container with improved layout
        button_frame = tk.Frame(prediction_frame, bg=self.style['bg_secondary'])
        button_frame.pack(pady=20)
        
        # Make buttons responsive
        button_frame.grid_columnconfigure((0,1,2), weight=1)

        # Styled buttons with grid layout
        calculate_btn = self.create_styled_button(
            button_frame,
            "💫 Calculate Value",
            self.predict_price,
            self.style['accent']
        )
        calculate_btn.grid(row=0, column=0, padx=10)

        reset_btn = self.create_styled_button(
            button_frame,
            "🔄 Reset",
            self.reset_fields,
            self.style['highlight']
        )
        reset_btn.grid(row=0, column=1, padx=10)

        save_btn = self.create_styled_button(
            button_frame,
            "💾 Save",
            self.save_estimate,
            self.style['success']
        )
        save_btn.grid(row=0, column=2, padx=10)

    def predict_price(self):
        try:
            # Validate and collect inputs
            input_values = []
            for feature, var in self.features.items():
                value = var.get().strip()
                if not value:
                    raise ValueError(f"Please enter a value for {feature}")
                try:
                    float_value = float(value)
                    if float_value < 0:
                        raise ValueError(f"{feature} cannot be negative")
                    input_values.append(float_value)
                except ValueError:
                    raise ValueError(f"Please enter a valid number for {feature}")

            # Scale input and predict
            input_scaled = self.scaler.transform(np.array([input_values]))
            prediction = self.model.predict(input_scaled)[0]

            # Format prediction
            formatted_price = self.format_indian_currency(prediction)
            self.show_result_popup(formatted_price)

        except Exception as e:
            self.result_label.configure(
                text=str(e),
                fg='red'
            )

    def format_indian_currency(self, amount):
        amount = abs(int(amount))
        s = str(amount)
        l = len(s)
        if l > 7:
            crores = s[:-7]
            remaining = s[-7:]
            formatted = crores + ',' + remaining[:2] + ',' + remaining[2:4] + ',' + remaining[4:]
        elif l > 5:
            lakhs = s[:-5]
            remaining = s[-5:]
            formatted = lakhs + ',' + remaining[:2] + ',' + remaining[2:]
        elif l > 3:
            formatted = s[:-3] + ',' + s[-3:]
        else:
            formatted = s
        return formatted

    def show_result_popup(self, formatted_price):
        popup = tk.Toplevel(self.root)
        popup.title("Property Valuation Result")
        popup.geometry("500x400")
        popup.configure(bg=self.style['bg_primary'])

        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        self.root.eval(f'tk::PlaceWindow {str(popup)} center')

        # Result display
        tk.Label(
            popup,
            text="Estimated Property Value",
            font=("Helvetica", 24, "bold"),
            fg=self.style['accent'],
            bg=self.style['bg_primary']
        ).pack(pady=20)

        tk.Label(
            popup,
            text=f"₹ {formatted_price}",
            font=("Helvetica", 36, "bold"),
            fg=self.style['accent'],
            bg=self.style['bg_primary']
        ).pack(pady=20)

        tk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            font=("Helvetica", 12, "bold"),
            bg=self.style['accent'],
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(pady=20)

    def create_styled_button(self, parent, text, command, color):
        frame = tk.Frame(parent, bg=self.style['bg_secondary'])
        
        # Create gradient effect for button
        btn = tk.Button(
            frame,
            text=text,
            command=command,
            font=("Helvetica", 12, "bold"),
            bg=color,
            fg=self.style['text_primary'],
            pady=12,
            padx=24,
            relief='flat',
            cursor='hand2',
            activebackground=self.style['accent_light'],
            activeforeground=self.style['bg_primary']
        )
        
        # Enhanced hover effect
        def on_enter(e):
            btn.configure(
                bg=self.style['accent_light'],
                fg=self.style['bg_primary']
            )
        def on_leave(e):
            btn.configure(
                bg=color,
                fg=self.style['text_primary']
            )
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        btn.pack(padx=2, pady=2)
        return frame

    def get_feature_icon(self, feature):
        icons = {
            'Square_Footage': '📏',
            'Bedrooms': '🛏️',
            'Bathrooms': '🚿',
            'Location_Rating': '📍',
            'Age of Property': '🏛️',
            'Floor_Number': '🏢',
            'Parking_Spots': '🚗',
            'Swimming_Pool': '🏊',
            'Garden Area': '🌳',
            'Smart Home Features': '🏠',
            'Security_Rating': '🔒',
            'View Rating': '🌅'
        }
        for key, icon in icons.items():
            if key in feature:
                return icon
        return '✨'

    def _on_mousewheel(self, event):
        # Improved smooth scrolling
        delta = int(-1 * (event.delta/120))
        self.main_canvas.yview_scroll(delta, "units")

    def reset_fields(self):
        for var in self.features.values():
            var.set('')
        self.result_label.configure(
            text="Enter property details and click Calculate",
            fg=self.style['text_primary']
        )

    def save_estimate(self):
        # Placeholder for save functionality
        pass

    def initialize_model(self):
        # Generate sample data for demonstration
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic features
        X = np.random.rand(n_samples, 8)  # 8 features
        
        # Generate synthetic prices based on the 8 features we have
        y = (
            X[:, 0] * 5000000 +  # Square Footage
            X[:, 1] * 2000000 +  # Bedrooms
            X[:, 2] * 1500000 +  # Bathrooms
            X[:, 3] * 3000000 +  # Location Rating
            X[:, 4] * 500000 +   # Floor Number
            X[:, 5] * 800000 +   # Parking Spots
            X[:, 6] * 2000000 +  # Swimming Pool
            X[:, 7] * 2000000    # Security Rating
        )
        
        # Add some noise
        y += np.random.normal(0, 500000, n_samples)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train the model
        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)

    def smooth_scroll(self, *args):
        # Smooth scrolling implementation
        self.main_canvas.yview_moveto(args[0])
        self.root.update_idletasks()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HousePricePredictionApp(root)
    root.mainloop()