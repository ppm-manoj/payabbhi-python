from ..error import InvalidRequestError
from .api_resource import APIResource


class Payment(APIResource):

    def __init__(self, client=None):
        super(Payment, self).__init__(client)

    def all(self, data=None, **kwargs):
        """"
        Get all Payments
        Args:
            data : Dictionary having keys using which payment list will be filtered
                count:           Count of payments to be retrieved
                skip:            Number of payments to be skipped
                to:              Payment list till this timestamp will be retrieved
                from:            Payment list from this timestamp will be retrieved
        Returns:
            List of Payment objects
        """
        if data is None:
            data = {}

        return super(Payment, self)._all(data, **kwargs)

    def retrieve(self, payment_id, **kwargs):
        """"
        Retrieve payment for given Id
        Args:
            payment_id : Id for which Payment object has to be retrieved
        Returns:
            Payment object with given payment Id
        """
        return self._retrieve(payment_id, **kwargs)

    def refunds(self, payment_id, data=None, **kwargs):
        """"
        Retrieve Refunds for given payment Id
        Args:
            payment_id: Payment identifier for which refunds has to be retrieved
            data : Dictionary having keys using which refund list will be filtered
                count:           Count of refunds to be retrieved
                skip:            Number of refunds to be skipped
                to:              Refund list till this timestamp will be retrieved
                from:            Refund list from this timestamp will be retrieved
        Returns:
            Refund list for a payment object
        """
        if data is None:
            data = {}

        url = "{0}/refunds".format(self.instance_url(payment_id))
        return self._get(url, data, **kwargs)

    def virtual_account(self, payment_id, data=None, **kwargs):
        """"
        Retrieve virtual_account details for given payment Id
        Args:
            payment_id: Payment identifier for which virtual_account details has to be retrieved
        Returns:
            Returns a payment object, given a valid payment identifier was provided, and returns
            an error otherwise.
        """
        if data is None:
            data = {}

        url = "{0}/virtual_account".format(self.instance_url(payment_id))
        return self._get(url, data, **kwargs)

    def capture(self, data=None, **kwargs):
        """"
        Captures the Payment object
        Returns:
            Updated Payment object after getting captured
        """
        if data is None:
            data = {}

        if not hasattr(self, 'id'):
            raise InvalidRequestError('Object Id not set')

        url = self.instance_url(self.id) + '/capture'
        captured_payment = self._post(url, data, **kwargs)
        self.__dict__.update(captured_payment.__dict__)

        return self

    def refund(self, data=None, **kwargs):
        """"
        Refunds Payment object with given data
        Args:
            data : Dictionary having keys using which payment has to be refunded
                amount : Amount for which the payment has to be refunded
                notes: Key value pair as notes
        Returns:
            Refund object that is created
        """
        if data is None:
            data = {}

        if not hasattr(self, 'id'):
            raise InvalidRequestError('Object Id not set')

        url = self.instance_url(self.id) +'/refunds'
        refund = self._post(url, data, **kwargs)

        refunded_payment = self._retrieve(self.id)
        self.__dict__.update(refunded_payment.__dict__)

        return refund

    def transfer(self, source_id, data, **kwargs):
        """"
        Create Transfer from given data
        Args:
            source_id: The identifier of the source for which transfers need to be created.
            data : Dictionary having keys using which transfer has to be created
                transfers: List of transfers to be created with following details
                recipient_id: The identifier of recipient of this transfer
                description: Description of the Transfer.
                amount:  Amount of Transfer
                currency: Currency used in Transfer
                notes: key value pair as notes
        Returns:
            Transfer object containing data for created transfers
        """
        url = "{0}/transfer".format(self.instance_url(source_id))
        return self._post(url, data, **kwargs)


    def transfers(self, payment_id, data=None, **kwargs):
        """"
        Retrieve Transfers for given payment Id
        Args:
            payment_id: Payment identifier for which transfers has to be retrieved
            data : Dictionary having keys using which transfer list will be filtered
                count:           Count of transfers to be retrieved
                skip:            Number of transfers to be skipped
                to:              Transfer list till this timestamp will be retrieved
                from:            Transfer list from this timestamp will be retrieved
        Returns:
            Transfer list for a payment object
        """
        if data is None:
            data = {}

        url = "{0}/transfers".format(self.instance_url(payment_id))
        return self._get(url, data, **kwargs)
