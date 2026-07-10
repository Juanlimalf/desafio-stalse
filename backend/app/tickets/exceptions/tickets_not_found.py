class TicketsNotFoundError(Exception):
    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        self.message = f"Ticket with ID {ticket_id} not found."
        super().__init__(self.message)
