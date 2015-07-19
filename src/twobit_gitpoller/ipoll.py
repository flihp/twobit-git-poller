class IPoll(object):
    """ The IPoll interface type.
    """
    def poll(self):
        """ A repeated action.
        """
        raise NotImplementedError("Inherited from IPoll but 'poll' method not implemented")
