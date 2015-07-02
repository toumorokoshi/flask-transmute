==========
decorators
==========

flask-transmute attempts to extract as much information as possible from the
function declaration itself. However, there are times when behaviour should
be indicated that is not clear from the function signature.

to accomodate this, flask-transmute provides decorators to help describe additional
behavior:


.. code:: python

    import flask_transmute

    cards = []

    # create indicates data is being created,
    # correlated to a PUT request
    @flask_transmute.creates
    def create_card(card: str) -> bool:
         cards.append(card)
         return True

    # updates indicates data is being updated,
    # correlated to a POST request
    @flask_transmute.updates
    def update_card(old_card: str, new_card: str) -> bool:
        if old_card in cards:
            card_index = cards.index(old_card)
            cards.remove(old_card)
            cards.insert(card_index, new_card)
            return True
        return False

    # deletes indicates data is being deleted,
    # correlated to a DELETE request
    @flask_transmute.deletes
    def delete_card(card: str) -> bool:
        if card in cards:
            cards.remove(card)
            return True
        return False

    # in Python 2, it is not possible to annotate functions. flask_transmute
    # provides a decorator to help with that
    @flask_transmute.creates
    @flask_transume.annotates({"card": str, "return": bool})
    def create_card(card):
        cards.append(card)
        return True
