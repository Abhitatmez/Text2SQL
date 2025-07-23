// API Base URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// DOM Elements
const queryInput = document.getElementById('queryInput');
const sqlInput = document.getElementById('sqlInput');
const generateBtn = document.getElementById('generateBtn');
const executeBtn = document.getElementById('executeBtn');
const queryBtn = document.getElementById('queryBtn');
const copySqlBtn = document.getElementById('copySqlBtn');
const copyToSqlInputBtn = document.getElementById('copyToSqlInputBtn');

// Results elements
const sqlResults = document.getElementById('sqlResults');
const sqlQuery = document.getElementById('sqlQuery');
const confidence = document.getElementById('confidence');
const estimatedRows = document.getElementById('estimatedRows');
const explanation = document.getElementById('explanation');

const queryResults = document.getElementById('queryResults');
const rowCount = document.getElementById('rowCount');
const executionTime = document.getElementById('executionTime');
const tableHead = document.getElementById('tableHead');
const tableBody = document.getElementById('tableBody');

const errorDisplay = document.getElementById('errorDisplay');
const errorMessage = document.getElementById('errorMessage');
const resultsPlaceholder = document.getElementById('resultsPlaceholder');

// State
let currentSqlQuery = '';
let currentQuery = '';

// Event Listeners
generateBtn.addEventListener('click', handleGenerateSQL);
executeBtn.addEventListener('click', handleExecuteSQL);
queryBtn.addEventListener('click', handleQuery);
copySqlBtn.addEventListener('click', copySQLToClipboard);
copyToSqlInputBtn.addEventListener('click', copyToSqlInput);
queryInput.addEventListener('keydown', handleKeyPress);

// Handle Enter key to generate SQL
function handleKeyPress(event) {
    if (event.key === 'Enter' && event.ctrlKey) {
        event.preventDefault();
        handleQuery(); // Use the main query endpoint by default
    }
}

// Generate SQL from natural language
async function handleGenerateSQL() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a natural language query.');
        return;
    }

    currentQuery = query;
    setLoading(generateBtn, true);
    hideAllResults();

    try {
        const response = await fetch(`${API_BASE_URL}/generate-sql`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (response.ok) {
            displaySQLResults(data);
            currentSqlQuery = data.sql_query;
        } else {
            showError(`Error: ${data.detail || 'Failed to generate SQL'}`);
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        setLoading(generateBtn, false);
    }
}

// Execute the generated SQL
async function handleExecuteSQL() {
    const sqlQuery = sqlInput.value.trim();
    
    if (!sqlQuery) {
        showError('Please enter a SQL query to execute.');
        return;
    }

    setLoading(executeBtn, true);
    hideResults(queryResults);
    hideResults(errorDisplay);

    try {
        const response = await fetch(`${API_BASE_URL}/execute-sql`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sql_query: sqlQuery })
        });

        const data = await response.json();
        console.log('Execute SQL Response:', data); // Debug log

        if (response.ok) {
            // Handle the actual API response format
            if (data.success) {
                console.log('Displaying results:', data.data); // Debug log
                displayQueryResults({
                    results: data.data || [],
                    columns: data.data && data.data.length > 0 ? Object.keys(data.data[0]) : [],
                    execution_time: data.execution_time_ms
                });
            } else {
                showError(`Error: ${data.error_message || 'Failed to execute SQL'}`);
            }
        } else {
            showError(`Error: ${data.detail || 'Failed to execute SQL'}`);
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        setLoading(executeBtn, false);
    }
}

// Main query function - Generate SQL and execute in one step
async function handleQuery() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a natural language query.');
        return;
    }

    currentQuery = query;
    setLoading(queryBtn, true);
    hideAllResults();

    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                query: query,
                include_sql: true
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Display both SQL and results
            displaySQLResults({
                sql_query: data.sql_query,
                confidence: data.confidence,
                estimated_rows: data.estimated_rows,
                explanation: data.explanation
            });
            
            // Display query results if available (handle both response formats)
            if (data.success && data.data && data.data.length > 0) {
                // New format from /query endpoint
                displayQueryResults({
                    results: data.data,
                    columns: Object.keys(data.data[0]),
                    execution_time: data.execution_time_ms
                });
            } else if (data.results && data.results.length > 0) {
                // Old format fallback
                displayQueryResults({
                    results: data.results,
                    columns: data.columns,
                    execution_time: data.execution_time
                });
            }
            
            currentSqlQuery = data.sql_query;
        } else {
            showError(`Error: ${data.detail || 'Failed to process query'}`);
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        setLoading(queryBtn, false);
    }
}

// Display SQL generation results
function displaySQLResults(data) {
    sqlQuery.textContent = data.sql_query;
    confidence.textContent = `${(data.confidence * 100).toFixed(1)}%`;
    estimatedRows.textContent = data.estimated_rows || 'Unknown';
    explanation.textContent = data.explanation || 'No explanation available.';

    // Auto-fill the SQL input field for manual execution
    sqlInput.value = data.sql_query;

    showResults(sqlResults);
    hideResults(errorDisplay);
    hideResults(resultsPlaceholder);
}

// Display query execution results
function displayQueryResults(data) {
    const results = data.results || [];
    const columns = data.columns || [];
    
    // Update metadata
    rowCount.textContent = `${results.length} row${results.length !== 1 ? 's' : ''}`;
    executionTime.textContent = data.execution_time ? `${data.execution_time}ms` : '';

    // Create table header
    tableHead.innerHTML = '';
    const headerRow = document.createElement('tr');
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });
    tableHead.appendChild(headerRow);

    // Create table body
    tableBody.innerHTML = '';
    results.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(column => {
            const td = document.createElement('td');
            td.textContent = row[column] !== null ? row[column] : 'NULL';
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });

    showResults(queryResults);
    hideResults(resultsPlaceholder);
}

// Copy SQL to clipboard
async function copySQLToClipboard() {
    try {
        const sqlToCopy = currentSqlQuery || sqlQuery.textContent;
        if (!sqlToCopy) {
            showError('No SQL query to copy');
            return;
        }
        
        await navigator.clipboard.writeText(sqlToCopy);
        
        // Enhanced visual feedback
        const originalText = copySqlBtn.textContent;
        const originalClasses = copySqlBtn.className;
        
        copySqlBtn.innerHTML = '✓ Copied!';
        copySqlBtn.className = originalClasses + ' btn-success';
        
        // Add subtle animation
        copySqlBtn.style.transform = 'scale(1.1)';
        
        setTimeout(() => {
            copySqlBtn.style.transform = 'scale(1)';
        }, 150);
        
        setTimeout(() => {
            copySqlBtn.textContent = originalText;
            copySqlBtn.className = originalClasses;
        }, 2500);
    } catch (error) {
        showError('Failed to copy SQL to clipboard');
    }
}

// Copy SQL to SQL input field
function copyToSqlInput() {
    const sqlToCopy = currentSqlQuery || sqlQuery.textContent;
    if (!sqlToCopy) {
        showError('No SQL query to copy');
        return;
    }
    
    sqlInput.value = sqlToCopy;
    
    // Enhanced visual feedback
    const originalText = copyToSqlInputBtn.textContent;
    const originalClasses = copyToSqlInputBtn.className;
    
    copyToSqlInputBtn.innerHTML = '✓ Added to Input!';
    copyToSqlInputBtn.className = originalClasses + ' btn-success';
    
    // Add subtle animation
    copyToSqlInputBtn.style.transform = 'scale(1.1)';
    
    setTimeout(() => {
        copyToSqlInputBtn.style.transform = 'scale(1)';
    }, 150);
    
    setTimeout(() => {
        copyToSqlInputBtn.textContent = originalText;
        copyToSqlInputBtn.className = originalClasses;
    }, 2500);
    
    // Scroll to SQL input section with enhanced animation
    sqlInput.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
    });
    
    // Add focus highlight to SQL input
    sqlInput.focus();
    setTimeout(() => {
        sqlInput.style.transform = 'scale(1.02)';
        sqlInput.style.transition = 'transform 0.3s ease';
        setTimeout(() => {
            sqlInput.style.transform = 'scale(1)';
        }, 300);
    }, 500);
}

// Utility functions
function setLoading(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
        button.disabled = true;
    } else {
        btnText.style.display = 'flex';
        btnLoading.style.display = 'none';
        button.disabled = false;
    }
}

function showResults(element) {
    element.style.display = 'block';
}

function hideResults(element) {
    element.style.display = 'none';
}

function hideAllResults() {
    hideResults(sqlResults);
    hideResults(queryResults);
    hideResults(errorDisplay);
    showResults(resultsPlaceholder);
}

function showError(message) {
    errorMessage.textContent = message;
    showResults(errorDisplay);
    hideResults(sqlResults);
    hideResults(queryResults);
    hideResults(resultsPlaceholder);
}

// Initialize the UI
document.addEventListener('DOMContentLoaded', function() {
    // Add some example queries for quick testing
    const examples = [
        'Show me all customers from Mumbai',
        'Find products with price above ₹1000',
        'List orders from last month',
        'Show top 5 customers by total order amount',
        'Find products in Electronics category'
    ];

    // Add example buttons (optional enhancement)
    // You can uncomment this to add quick example buttons
    /*
    const exampleContainer = document.createElement('div');
    exampleContainer.className = 'example-queries';
    exampleContainer.innerHTML = '<h3>Quick Examples:</h3>';
    
    examples.forEach(example => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-small';
        btn.textContent = example;
        btn.onclick = () => {
            queryInput.value = example;
            handleGenerateSQL();
        };
        exampleContainer.appendChild(btn);
    });
    
    document.querySelector('.input-section').appendChild(exampleContainer);
    */
});

// Function to set example text
function setExample(text) {
    queryInput.value = text;
    queryInput.focus();
    // Add a subtle highlight effect
    queryInput.style.transform = 'scale(1.01)';
    queryInput.style.borderColor = 'rgba(59, 130, 246, 0.6)';
    setTimeout(() => {
        queryInput.style.transform = 'scale(1)';
        queryInput.style.borderColor = '';
    }, 300);
}

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 