## 🚀 Chamatech

**Odoo 19 | Chama Management System**

Chamatech is a minimalist Odoo module designed to automate and manage community-based savings and investment groups (Chamas). It provides a structured way to track member contributions, financial goals, and payment statuses.

---

### 🛠️ Key Features

- **Contribution Tracking**: Log names, specific amounts, and payment frequencies.
    
- **Status Workflows**: Real-time tracking of payments (e.g., Draft, Paid, Overdue) via a dynamic status bar.
    
- **Optimized UI**:
    
    - **List View**: High-level overview of group finances.
        
    - **Form View**: Detailed record management using Odoo’s `<sheet>` and `<group>` architecture for a clean "paper" feel.
        

---

### 📂 Project Structure

```
chamatech/
├── models/
│   └── chamatech.py      # Data models and field definitions
├── views/
│   └── views.xml         # XML definitions for List, Form, and Menus
├── security/
│   └── ir.model.access.csv # Access rights for the chamatech model
├── __init__.py           # Python package initialization
└── __manifest__.py       # Module metadata (name, version, dependencies)
```

---

### 🏗️ Installation Guide

1. **Move the Module**: Copy the `chamatech` folder into your Odoo `addons` directory.
    
2. **Update Permissions**: Ensure the folder has the correct read/write permissions for your Odoo user.
    
3. **Restart & Upgrade**:
    
    Run the following command in your terminal to initialize the module:
    
    Bash
    
    ```
   ./odoo-bin -u chamatech
    ```
    
4. **Activate**:
    
    - Log in to your Odoo instance as an **Administrator**.
        
    - Activate **Developer Mode**.
        
    - Go to **Apps**, search for "Chamatech", and click **Activate**.
        

---
