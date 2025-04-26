# necessary modules
from email_validation import EmailValidator

# driver function
def main():
    # Instantiate EmailValidator class
    validator = EmailValidator()
    
    # prompts user  one or more emails to validate
    emails = validator.get_emails_list()
    
    # Validate emails
    # Bulk email validation
    results = validator.validate_bulk_emails(emails)
    
    # printing results
    for res in results:
        print(res)    


# Run driver function
if __name__ == "__main__":
    main()    