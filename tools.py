from langchain_core.tools import tool
import random

@tool
def lookup_invoice(invoice_id: str) -> str:
    """Look up invoice details by ID. Returns status and amount."""
    # Mock data
    if invoice_id.startswith("INV-"):
        return f"Invoice {invoice_id}: Status=Unpaid, Amount=$50.00, Date=2023-10-01"
    return "Invoice not found."

@tool
def process_refund(invoice_id: str) -> str:
    """Process a refund for a given invoice ID."""
    if invoice_id.startswith("INV-"):
        return f"Refund processed for {invoice_id}. Transaction ID: REF-{random.randint(1000, 9999)}"
    return "Invalid invoice ID for refund."

@tool
def check_server_status(server_id: str) -> str:
    """Check the health status of a specific server."""
    statuses = ["Online", "Degraded", "Offline", "Maintenance"]
    return f"Server {server_id} is currently: {random.choice(statuses)}"

@tool
def search_knowledge_base(query: str) -> str:
    """Search the technical knowledge base for articles."""
    # Mock results
    return f"Found article for '{query}': 'How to restart the daemon' (Link: /kb/123). Summary: Sudo systemctl restart..."
