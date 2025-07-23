# Text2SQL Assistant - Web UI

A beautiful, modern web interface for the Text2SQL Assistant that allows you to convert natural language queries to SQL and execute them with a single click.

## Features

- **Glass Morphism Design**: Modern, elegant UI with glass-like effects
- **Black & White Theme**: Clean, professional design with serif fonts
- **Real-time SQL Generation**: Convert natural language to SQL instantly
- **Query Execution**: Execute generated SQL and view results in a table
- **Copy to Clipboard**: One-click SQL copying for external use
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Error Handling**: Clear error messages and validation feedback

## How to Use

### 1. Start the Application
```bash
python -m app.main
```

### 2. Access the UI
Open your browser and go to: `http://localhost:8000`

### 3. Using the Interface

#### Step 1: Enter Your Query
- Type your natural language question in the text area
- Examples:
  - "Show me all customers from Mumbai"
  - "Find products with price above ₹1000"
  - "List orders from last month"
  - "Show top 5 customers by total order amount"

#### Step 2: Generate SQL
- Click the **"Generate SQL"** button
- The system will convert your query to SQL
- You'll see the generated SQL, confidence score, and explanation

#### Step 3: Execute Query (Optional)
- Click the **"Execute Query"** button to run the SQL
- View results in a formatted table
- See row count and execution time

### 4. Additional Features

- **Copy SQL**: Click the "Copy SQL" button to copy the generated SQL to clipboard
- **Keyboard Shortcut**: Press `Ctrl + Enter` to generate SQL quickly
- **Database Schema**: View available tables and their structure at the bottom

## UI Components

### Input Section
- Large text area for natural language queries
- Generate SQL and Execute Query buttons
- Loading indicators during API calls

### Results Section
- **SQL Results**: Shows generated SQL with confidence and explanation
- **Query Results**: Displays executed query results in a table format
- **Error Display**: Shows validation and execution errors

### Database Schema
- Information about available tables
- Column descriptions for reference

## Design Features

### Glass Morphism
- Semi-transparent backgrounds with blur effects
- Subtle borders and shadows
- Hover animations and transitions

### Typography
- **Playfair Display**: Elegant serif font for headings
- **Source Serif Pro**: Clean serif font for body text
- **Courier New**: Monospace font for SQL code

### Color Scheme
- Light beige background gradient
- Black text for maximum readability
- Subtle grays for secondary information

### Responsive Design
- Mobile-first approach
- Flexible layouts that adapt to screen size
- Touch-friendly buttons and inputs

## Technical Details

### File Structure
```
app/static/
├── index.html      # Main HTML structure
├── styles.css      # Glass morphism CSS styles
└── script.js       # JavaScript functionality
```

### API Integration
- Connects to FastAPI backend at `http://localhost:8000/api/v1`
- Uses fetch API for HTTP requests
- Handles loading states and error responses

### Browser Compatibility
- Modern browsers with ES6+ support
- Requires clipboard API for copy functionality
- Responsive design works on all screen sizes

## Troubleshooting

### UI Not Loading
- Ensure the FastAPI server is running
- Check that static files are in the correct location
- Verify the server is accessible at `http://localhost:8000`

### API Errors
- Check that the backend API is running
- Verify your Gemini API key is set in `.env`
- Ensure the database is properly initialized

### Copy Function Not Working
- Some browsers require HTTPS for clipboard access
- Try using the keyboard shortcut `Ctrl+C` on the SQL code instead

## Customization

### Changing Colors
Edit `styles.css` to modify the color scheme:
```css
/* Main background */
body {
    background: linear-gradient(135deg, #your-color 0%, #your-color 100%);
}

/* Glass card background */
.glass-card {
    background: rgba(255, 255, 255, 0.25);
}
```

### Adding Features
- Modify `script.js` to add new functionality
- Update `index.html` for new UI elements
- Extend `styles.css` for additional styling

## Performance

- Optimized for fast loading
- Minimal external dependencies
- Efficient DOM manipulation
- Responsive image and font loading

The UI provides a seamless experience for converting natural language to SQL queries with a beautiful, professional interface that matches modern design standards. 