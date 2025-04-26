import re
import dns.resolver
from typing import List, Dict, Union


class EmailValidator:
    """
    A class to validate email addresses.
    Supports syntax validation and domain verification.
    """
      
    # Constructor
    def __init__(self):
        # Regular expression for basic email syntax validation
        self.email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                
         # Private, unknown or custom domains, to the concerned organization
        # Such domains can be hard coded or coded on runtime.
        self.local_domains_list: List[str] = []
        
        # List of emails to validate
        self.emails_list: List[str] = []
        
    # get email list from user
    def get_emails_list(self) -> List[str]:
        emails = input("Enter the emails to check separated by space: ").strip().split()
        for email in emails:
            self.emails_list.append(email)
        return self.emails_list
        
    # Email syntax check method
    def is_valid_syntax(self, email: str) -> bool:
        """
        Check if the email address has a valid syntax.
        :param email: Email address to validate
        :return: True if the syntax is valid, False otherwise
        """
        return re.match(self.email_regex, email) is not None
    
    # Set the private domain
    def set_local_domains(self) -> None:
        private_domains = input("Enter the private domains that concern your organization: ").strip().split()
        for domain in private_domains:
            self.local_domains_list.append(domain)
            
    # Retrieve local domains
    def get_localDomains(self) -> list:
        return self.local_domains_list

    # method to check the validity of the domain of an email
    def domain_exists(self, domain: str) -> bool:
        """
        Check if the domain has valid MX (Mail Exchange) records.
        :param domain: Domain part of the email address
        :return: True if the domain has MX records, False otherwise
        """
        if domain in self.get_localDomains():
            return True
        else:            
            try:
                # Query MX records for the domain
                mx_records = dns.resolver.resolve(domain, 'MX')
                return bool(mx_records)
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                return False

    # method to check email syntax and domain
    def validate_email(self, email: str) -> dict:
        """
        Validate an email address by checking its syntax and domain.
        :param email: Email address to validate
        :return: A dictionary with validation results
        
        """
        # validate each email in the email list            
        if not self.is_valid_syntax(email):
            return {"email": email, "isValid": False, "message": "Invalid email syntax."}

        domain = email.split('@')[1]
        if not self.domain_exists(domain):
            return {"email": email, "isValid": False, "message": "Invalid domain or domain does not exist."}

        return {"email": email, "isValid": True, "message": "Email is valid."}

    # Validate bulk emails entered by user
    def validate_bulk_emails(self, emails) -> List[Dict[str, Union[str, bool]]]:
        """
        Validate a list of email addresses.
        :param emails: List of email addresses to validate
        :return: List of validation results for each email
        """        
        results = list()
        for email in emails:
            results.append(self.validate_email(email))
        return results