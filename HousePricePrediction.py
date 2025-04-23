import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk     
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import urllib.request
from io import BytesIO

class HousePricePredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("K.R.M.U Property Price Predictor")
        
       
        self.style = {
            'bg_primary': '#000000',        # Pure black
            'bg_secondary': '#0A0A0A',      # Soft black
            'accent': '#FF2E63',            # Neon pink
            'accent_light': '#00FFF5',      # Neon cyan
            'text_primary': '#FFFFFF',      # Pure white
            'text_secondary': '#E6F1FF',    # Ice white
            'highlight': '#1A1A1A',         # Soft black
            'success': '#00B4D8',           # Ocean blue
            'input_bg': '#0A192F',          # Dark navy input
            'gradient_start': '#000000',    # Black gradient start
            'gradient_end': '#112240',      # Navy gradient end
            'border': '#64FFDA',            # Cyan border
            'label_text': '#FFFFFF'         # Pure white text
        }

        # Set window size and position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1024, 768)
        
        # Initialize features
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

        # Rest of the initialization
        self.initialize_model()
        self.root.configure(bg=self.style['bg_primary'])
        
        # Create main containers and UI elements
        self.main_canvas = tk.Canvas(
            root,
            bg=self.style['bg_primary'],
            highlightthickness=0
        )
        self.main_canvas.pack(side="left", fill="both", expand=True)

        self.main_container = tk.Frame(
            self.main_canvas,
            bg=self.style['bg_primary']
        )
        self.main_container.pack(expand=True, fill='both', padx=30, pady=30)

        # Create UI sections
        self.create_glass_effect_header()
        self.create_glass_effect_content()
        self.create_prediction_section()

    def create_gradient_background(self, width, height):
        gradient_canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            highlightthickness=0
        )
        gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a more vibrant gradient
        for i in range(0, height, 2):
            ratio = i / height
            if ratio < 0.5:
                color = self.interpolate_color('#0A192F', '#112240', ratio * 2)
            else:
                color = self.interpolate_color('#112240', '#1A2F4E', (ratio - 0.5) * 2)
            gradient_canvas.create_line(0, i, width, i, fill=color)

    def create_glass_effect_header(self):
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent",
            corner_radius=15
        )
        header_frame.pack(fill='x', pady=(0, 20))

        # Add decorative elements
        for i in range(2):
            accent_line = ctk.CTkFrame(
                header_frame,
                height=3,
                fg_color=self.style['accent'],
                corner_radius=1
            )
            accent_line.pack(fill='x', pady=(10 
                                             if i == 0 else 5), padx=100)

        self.header_label = ctk.CTkLabel(
            header_frame,
            text="✨ Premium Property Valuation ✨",
            font=("Helvetica", 42, "bold"),
            text_color=self.style['accent'],
        )
        self.header_label.pack(pady=20)
        self.animate_header()

    def animate_header(self):
        # Updated animation colors for more dramatic effect
        colors = ['#FF2E63', '#00FFF5', '#FFFFFF']  # Neon pink, cyan, and white
        current_color = 0
        
        def update_color():
            nonlocal current_color
            self.header_label.configure(text_color=colors[current_color])
            current_color = (current_color + 1) % 3
            self.root.after(800, update_color)  # Slightly faster animation
        
        update_color()

    def create_glass_effect_content(self):
        content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.style['bg_secondary'],
            corner_radius=15,
            border_width=2,
            border_color=self.style['accent']
        )
        content_frame.pack(fill='both', expand=True, pady=10)

        # Add glowing effect
        glow_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.style['accent'],
            corner_radius=15,
            height=4
        )
        glow_frame.pack(fill='x', padx=20, pady=(0, 20))

        # Glowing separator
        separator = ctk.CTkFrame(
            content_frame,
            height=2,
            fg_color=self.style['accent'],
            corner_radius=1
        )
        separator.pack(fill='x', pady=(0, 10), padx=20)

        # Create grid container
        grid_frame = tk.Frame(content_frame, bg=self.style['bg_secondary'])
        grid_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Configure grid columns and rows with equal spacing
        for i in range(4):
            grid_frame.columnconfigure(i, weight=1, pad=20)
            grid_frame.rowconfigure(i, weight=1, pad=20)

        # Define create_3d_frame function first
        def create_3d_frame(parent):
            frame = tk.Frame(parent, bg=self.style['bg_secondary'])
            shadow = tk.Frame(frame, bg=self.style['border'], width=2)
            shadow.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
            shadow = tk.Frame(frame, bg=self.style['border'], height=2)
            shadow.place(relx=0, rely=1.0, relwidth=1.0, anchor='sw')
            return frame

        # Update the labels in create_glass_effect_content method
        label_texts = {
            'Square_Footage': 'Square Footage (sq ft) ',
            'Bedrooms': 'Bedrooms       (1-5)',
            'Bathrooms': 'No. of Bathrooms (1-4)',
            'Location_Rating': 'Location Rating (1-10)',
            'Floor_Number': 'Floor Number (1-20)',
            'Parking_Spots': 'No. of Parking Spots (0-2)',
            'Swimming_Pool': 'Swimming Pool (0/1)',
            'Security_Rating': 'Security Rating (1-10)'
        }

        # Create input fields in grid layout with fixed positions
        field_positions = {
            'Square_Footage': (0, 0),
            'Bedrooms': (0, 1),
            'Bathrooms': (0, 2),
            'Location_Rating': (0, 3),
            'Floor_Number': (1, 0),
            'Parking_Spots': (1, 1),
            'Swimming_Pool': (1, 2),
            'Security_Rating': (1, 3)
        }

        # Update input field creation with fixed positions
        for feature, var in self.features.items():
            row, col = field_positions[feature]
            frame = create_3d_frame(grid_frame)
            frame.grid(row=row, column=col, padx=20, pady=20, sticky='nsew')
            
            # Rest of the input field creation code remains the same
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
            
            entry = ctk.CTkEntry(
                entry_frame,
                textvariable=var,
                font=("Helvetica", 12),
                fg_color=self.style['input_bg'],
                text_color=self.style['text_primary'],
                border_color=self.style['border'],
                corner_radius=8,
                height=35
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
        popup.geometry("600x500")
        popup.configure(bg=self.style['bg_primary'])
        
        # Create 3D card effect
        result_frame = ctk.CTkFrame(
            popup,
            fg_color=self.style['bg_secondary'],
            corner_radius=15
        )
        result_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Animated price reveal
        price_label = ctk.CTkLabel(
            result_frame,
            text="₹ 0",
            font=("Helvetica", 48, "bold"),
            text_color=self.style['accent']
        )
        price_label.pack(pady=40)
        
        def animate_price(current=0, target=int(formatted_price.replace(',', ''))):
            if current < target:
                next_val = min(current + (target // 20), target)
                price_label.configure(text=f"₹ {self.format_indian_currency(next_val)}")
                popup.after(50, lambda: animate_price(next_val, target))
        
        animate_price()
        
        # Modern close button
        close_btn = ctk.CTkButton(
            result_frame,
            text="Close",
            command=popup.destroy,
            fg_color=self.style['highlight'],
            hover_color=self.style['accent_light'],
            corner_radius=10,
            height=40
        )
        close_btn.pack(pady=20)

        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        self.root.eval(f'tk::PlaceWindow {str(popup)} center')

        # Result display
        tk.Label(
            popup,
            text="Estimated Property Price",
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
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        btn = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            font=("Helvetica", 12, "bold"),
            fg_color=color,
            text_color='#FFFFFF',
            corner_radius=12,
            height=45,
            border_width=2,
            border_color=self.style['border']
        )
        
        btn.pack(padx=3, pady=3, fill='x')
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
        # More efficient scrolling
        self.main_canvas.yview_scroll(int(-1 * (event.delta/60)), "units")
        return "break"  # Prevent event propagation

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
        # Generate sample data based on Delhi real estate market
        np.random.seed(42)
        n_samples = 1000
        
        # Generate features with realistic ranges for Delhi
        square_footage = np.random.uniform(500, 4000, n_samples)  # 500-4000 sq ft
        bedrooms = np.random.randint(1, 6, n_samples)  # 1-5 bedrooms
        bathrooms = np.random.randint(1, 5, n_samples)  # 1-4 bathrooms
        location_rating = np.random.uniform(1, 10, n_samples)  # Location score
        floor_number = np.random.randint(1, 20, n_samples)  # 1-20 floors
        parking_spots = np.random.randint(0, 3, n_samples)  # 0-2 parking spots
        swimming_pool = np.random.randint(0, 2, n_samples)  # 0-1 (No/Yes)
        security_rating = np.random.uniform(1, 10, n_samples)  # Security score
    
        # Combine features
        X = np.column_stack([
            square_footage, bedrooms, bathrooms, location_rating,
            floor_number, parking_spots, swimming_pool, security_rating
        ])
        
        # Generate prices based on Delhi market rates (in INR)
        base_price_per_sqft = 12000  # Base price per sq ft in Delhi
        
        y = (
            square_footage * base_price_per_sqft +  # Base price by area
            bedrooms * 1000000 +                    # Premium for each bedroom
            bathrooms * 800000 +                    # Premium for each bathroom
            location_rating * 2000000 +             # Location premium
            floor_number * 200000 +                 # Floor premium
            parking_spots * 1500000 +               # Parking premium
            swimming_pool * 5000000 +               # Swimming pool premium
            security_rating * 1000000               # Security premium
        )
        
        # Add market variations (±10%)
        y += np.random.normal(0, 0.1 * y, n_samples)
        
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

    def create_gradient_background(self, width, height):
        gradient_canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            highlightthickness=0
        )
        gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Reduce number of gradient lines for better performance
        step = 2  # Increase step size for faster rendering
        for i in range(0, height, step):
            ratio = i / height
            color = self.interpolate_color(
                self.style['gradient_start'],
                self.style['gradient_end'],
                ratio
            )
            gradient_canvas.create_line(0, i, width, i, fill=color)

    def interpolate_color(self, color1, color2, ratio):
        # Fast color interpolation
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        return f'#{r:02x}{g:02x}{b:02x}'

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HousePricePredictionApp(root)
    root.mainloop()

    # Add resize handler
    self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        # Only handle window resize events
        if event.widget == self.root:
            # Update font sizes and layouts
            header_font_size = min(42, int(self.root.winfo_width() / 30))
            self.header_label.configure(font=("Helvetica", header_font_size, "bold"))
            
            # Update other responsive elements as needed
            self.update_responsive_layout()

    def update_responsive_layout(self):
        # Update padding and margins
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        self.main_container.pack_configure(
            padx=int(window_width * 0.05),
            pady=int(window_height * 0.03)
        )
