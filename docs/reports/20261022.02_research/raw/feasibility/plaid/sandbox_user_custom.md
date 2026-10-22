---
title: "Sandbox - Customize test data | Plaid Docs"
description: "Use custom Sandbox accounts to create rich testing data for the Assets, Auth, Balance, Identity, Liabilities, Transactions, and Investments products."
canonical: "https://plaid.com/docs/sandbox/user-custom/"
---

Create Sandbox test data 
=========================

#### Use Sandbox accounts to create rich test data for Plaid products 

#### Customize Sandbox account data 

In addition to a set of pre-populated [Sandbox test users](https://plaid.com/docs/sandbox/test-credentials/index.html.md) , the Sandbox environment also provides the ability to create custom user accounts, which can be used in conjunction with [/sandbox/public\_token/create](https://plaid.com/docs/api/sandbox/index.html.md#sandboxpublic_tokencreate) or Plaid Link to generate custom Sandbox data, or in conjunction with Plaid Link to test Link flows in the Sandbox. (A custom user is a set of test credentials, and is unrelated to the user object created by [/user/create](https://plaid.com/docs/api/users/index.html.md#usercreate) .)

Using these accounts, you can create your own testing data for the Assets, Auth, Balance, Identity, Investments, Liabilities, and Transactions products. You can also simulate an account with regular income or one that makes regular loan payments. For Link testing, custom accounts support multi-factor authentication, reCAPTCHA, and Link error flows.

To customize testing data for Document Income, see [Testing Document Income](https://plaid.com/docs/income/document-income/index.html.md#testing-document-income) .

#### Customizing account data using the Sandbox Studio 

The [Sandbox Studio](https://dashboard.plaid.com/developers/sandbox) tool in the Plaid Dashboard, under Build -> Sandbox, is a no-code way to work with Sandbox data. In the Dashboard, you can browse Plaid's built-in [test users](https://plaid.com/docs/sandbox/test-credentials/index.html.md) or create and edit your own custom users.

When creating a custom user in the Studio, you can describe the user you want in plain language and Plaid drafts the [configuration object](https://plaid.com/docs/sandbox/user-custom/index.html.md#configuration-object-schema) for you. You can keep refining the draft with follow-up prompts, start from one of the templates in the dropdown, or edit the JSON directly. Editing a saved custom user doesn't change Items already created with it.

To learn more about Sandbox Studio functionality, see [Sandbox Studio](https://plaid.com/docs/sandbox/studio/index.html.md) .

#### Configuring the custom user account 

Custom user accounts can be configured and accessed in two ways. The easiest (and recommended) method is by using [Sandbox Studio](https://plaid.com/docs/sandbox/studio/index.html.md) , located in the Plaid Dashboard under Build -> Sandbox. Set the username and [configuration object](https://plaid.com/docs/sandbox/user-custom/index.html.md#configuration-object-schema) on the **Users** tab, then go through the Link flow on Sandbox with that username and any non-empty password.

(An image of "A custom user's page on the Users tab of Sandbox Studio, showing its credentials, recent Items, connected account, and transactions.")

Alternatively, you can log into Sandbox with the username `user_custom` and provide the [JSON configuration object](https://plaid.com/docs/sandbox/user-custom/index.html.md#configuration-object-schema) as the password. While you can technically copy and paste a JSON object into the password field via the Sandbox Link UI, when using this approach, it is more common to bypass Link and create a public token directly by calling [/sandbox/public\_token/create](https://plaid.com/docs/api/sandbox/index.html.md#sandboxpublic_tokencreate) with `options.override_username` and `options.override_password`. This method is especially useful if you need to create test data programmatically or via AI-assisted tools.

To keep a configuration's dates current without editing them, see [Keeping transaction dates current](https://plaid.com/docs/sandbox/user-custom/index.html.md#keeping-transaction-dates-current) .

##### Limitations of the custom user account 

Very large configuration objects (larger than approximately 55kb, or approximately 250 transactions) are not supported and may cause the Link attempt to fail.

Using more than ten accounts on a single custom user is not supported and will cause the Link attempt to fail.

At OAuth institutions, custom users may not work properly: certain less frequently used customized fields may be overridden by the default values after the Link flow has completed, or the login may fail. If this occurs, retry the configuration using a non-OAuth institution, such as First Gingham Credit Union or First Platypus Bank.

[Prefer to learn by watching? Check out this quick video guide to Custom Sandbox Users](https://www.youtube.com/watch?v=viSyB5nww_s)

#### Keeping transaction dates current 

Custom user configurations use fixed dates, so over time a saved custom user's transactions can fall outside the Item's transaction history window. To keep them current, set `roll_dates_forward` to `true`. When the Item is created, Plaid moves the configuration's dates forward by the same amount, so the most recent activity lands on the creation date and the spacing between dates is preserved. Leave the flag off if your tests depend on the exact dates in the configuration.

Every date in the configuration shifts, including liability dates such as `next_payment_due_date`. Dates that Plaid derives from the Item's data, such as Bank Income streams, shift along with them. For example, if a configuration's latest transaction is dated 2026-06-10 and you create the Item on 2026-09-21, every date moves forward 103 days. A transaction whose `date_posted` is still in the future after the shift starts out pending.

The shift happens once, when the Item is created. Transactions you add later with [/sandbox/transactions/create](https://plaid.com/docs/api/sandbox/index.html.md#sandboxtransactionscreate) keep the dates you give them.

#### Configuration object schema 

(An image of "A custom user's configuration object, editable as JSON on the Users tab of Sandbox Studio, showing the override\_accounts array with a checking account's starting balance and identity data.")

Custom test accounts are configured with a JSON configuration object formulated according to the schema below. All top level fields are optional. Sending an empty object as a configuration will result in an account configured with random balances and transaction history.

**Properties**

integer

The version of the password schema to use, sent as a number. Possible values are `1` or `2`. The default value is `2`. You should only specify `1` if you know it is necessary for your test suite.

Minimum: `1`

Maximum: `2`

string

A seed, in the form of a string, that will be used to randomly generate account and transaction data, if this data is not specified using the `override_accounts` argument. If no seed is specified, the randomly generated data will be different each time.

Note that transactions data is generated relative to the Item's creation date. Different Items created on different dates with the same seed for transactions data will have different dates for the transactions. The number of days between each transaction and the Item creation will remain constant. For example, an Item created on December 15 might show a transaction on December 14. An Item created on December 20, using the same seed, would show that same transaction occurring on December 19.

boolean

When `true`, every date in this configuration is shifted at Item creation so that the most recent activity date falls on the day the Item is created, keeping the spacing between dates. Activity dates are transaction and investment transaction dates, pay period end dates and pay days, holding `institution_price_as_of` dates, and a loan's `last_payment_date` or `last_statement_issue_date`. Scheduled loan dates such as `origination_date`, `maturity_date`, and `next_payment_due_date` move by the same amount but are never the anchor. This lets a saved configuration keep producing recent data without being edited.

A `date_posted` later than its `date_transacted` stays later, so the most recent transaction can still be pending. Dates are UTC calendar dates. The shift happens once, when the Item is created; the Item keeps the shifted dates afterwards. Defaults to `false`.

Default: `false`

\[object\]

An array of account overrides to configure the accounts for the Item. By default, if no override is specified, transactions and account data will be randomly generated based on the account type and subtype, and other products will have fixed or empty data.

string

`investment:` Investment account.

`credit:` Credit card

`depository:` Depository account

`loan:` Loan account

`payroll:` Payroll account

`other:` Non-specified account type

See the [Account type schema](https://plaid.com/docs/api/accounts/index.html.md#account-type-schema) for a full listing of account types and corresponding subtypes.

Possible values: `investment`, `credit`, `depository`, `loan`, `payroll`, `other`

string

See the [Account type schema](https://plaid.com/docs/api/accounts/index.html.md#account-type-schema) for a full listing of account types and corresponding subtypes.

Possible values: `401a`, `401k`, `403B`, `457b`, `529`, `auto`, `brokerage`, `business`, `cash isa`, `cash management`, `cd`, `checking`, `commercial`, `commercial line of credit`, `construction`, `consumer`, `credit card`, `crypto exchange`, `ebt`, `education savings account`, `fhsa`, `fixed annuity`, `gic`, `health reimbursement arrangement`, `home equity`, `home equity loan`, `hsa`, `isa`, `ira`, `keogh`, `lif`, `life insurance`, `limited purpose checking`, `line of credit`, `lira`, `loan`, `lrif`, `lrsp`, `money market`, `mortgage`, `mutual fund`, `non-custodial wallet`, `non-taxable brokerage account`, `other`, `other insurance`, `other annuity`, `overdraft`, `paypal`, `payroll`, `pension`, `prediction market`, `prepaid`, `prif`, `profit sharing plan`, `qshr`, `rdsp`, `resp`, `retirement`, `rlif`, `roth`, `roth 401k`, `roth 403B`, `roth 457b`, `roth pension`, `roth profit sharing plan`, `roth thrift savings plan`, `rrif`, `rrsp`, `sarsep`, `savings`, `sep ira`, `simple ira`, `sipp`, `stock plan`, `student`, `thrift savings plan`, `tfsa`, `trust`, `ugma`, `utma`, `variable annuity`

number

If provided, the account will start with this amount as the current balance.

Format: `double`

number

If provided, the account will always have this amount as its available balance, regardless of current balance or changes in transactions over time. Cannot be set together with `has_null_available_balance`.

Format: `double`

boolean

If set to `true`, the account will always have null as its available balance, regardless of current balance or changes in transactions over time. Cannot be set together with `force_available_balance`.

string

ISO-4217 currency code. If provided, the account will be denominated in the given currency. Transactions will also be in this currency by default.

object

Allows specifying the metadata of the test account

string

The account's name

string

The account's official name

number

The account's limit

Format: `double`

string

The account's mask. Should be an empty string or a string of 2-4 alphanumeric characters. This allows you to model a mask which does not match the account number (such as with a virtual account number).

Pattern: `^$|^[A-Za-z0-9]{2,4}$`

number

The annual percentage yield (APY) to report on the account, expressed as a percentage (e.g. `4.25` means 4.25%). Applies to interest-bearing depository accounts; if omitted, the account reports no APY.

Format: `double`

object

Account and bank identifier number data used to configure the test account. All values are optional.

string

Will be used for the account number.

string

Must be a valid ACH routing number. To test `/transfer/capabilities/get`, set this to 322271627 to force a `true` result.

string

Must be a valid wire transfer routing number.

string

EFT institution number. Must be specified alongside `eft_branch`.

string

EFT branch number. Must be specified alongside `eft_institution`.

string

Business Identifier Code (BIC). Must be specified alongside `international_iban`.

string

International Bank Account Number (IBAN). If no account number is specified via `account`, will also be used as the account number by default. Must be specified alongside `international_bic`.

string

Bacs sort code

\[object\]

Specify the list of transactions on the account.

string

The date of the transaction, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. This field does not affect pending status; see `date_posted`.

Format: `date`

string

The date the transaction posted, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Posted dates in the past or present will result in posted transactions; posted dates in the future will result in pending transactions.

Format: `date`

number

The transaction amount. Can be negative.

Format: `double`

string

The transaction description.

string

The ISO-4217 format currency code for the transaction.

\[object\]

Specify the list of holdings on the account.

number

The last price given by the institution for this security

Format: `double`

string

The date at which `institution_price` was current. Must be formatted as an [ISO 8601](https://wikipedia.org/wiki/ISO_8601) date.

Format: `date`

number

The total cost basis of the holding (e.g., the total amount spent to acquire all assets currently in the holding).

Format: `double`

number

The total quantity of the asset held, as reported by the financial institution.

Format: `double`

string

Either a valid `iso_currency_code` or `unofficial_currency_code`

object

Specify the security associated with the holding or investment transaction. When inputting custom security data to the Sandbox, Plaid will perform post-data-retrieval normalization and enrichment. These processes may cause the data returned by the Sandbox to be slightly different from the data you input. An ISO-4217 currency code and a security identifier (`ticker_symbol`, `cusip`, or `isin`) are required.

string

12-character ISIN, a globally unique securities identifier. A verified CUSIP Global Services license is required to receive this data. This field will be null by default for new customers, and null for existing customers starting March 12, 2024. If you would like access to this field, please [request ISIN/CUSIP access here](https://docs.google.com/forms/d/e/1FAIpQLSd9asHEYEfmf8fxJTHZTAfAzW4dugsnSu-HS2J51f1mxwd6Sw/viewform) .

string

9-character CUSIP, an identifier assigned to North American securities. A verified CUSIP Global Services license is required to receive this data. This field will be null by default for new customers, and null for existing customers starting March 12, 2024. If you would like access to this field, please [request ISIN/CUSIP access here](https://docs.google.com/forms/d/e/1FAIpQLSd9asHEYEfmf8fxJTHZTAfAzW4dugsnSu-HS2J51f1mxwd6Sw/viewform) .

string

A descriptive name for the security, suitable for display.

string

The security's trading symbol for publicly traded securities, and otherwise a short identifier if available.

string

Either a valid `iso_currency_code` or `unofficial_currency_code`

\[object\]

Specify the list of investment transactions on the account.

string

Posting date for the transaction. Must be formatted as an [ISO 8601](https://wikipedia.org/wiki/ISO_8601) date.

Format: `date`

string

The institution's description of the transaction.

number

The number of units of the security involved in this transaction. Must be positive if the type is a buy and negative if the type is a sell.

Format: `double`

number

The price of the security at which this transaction occurred.

Format: `double`

number

The combined value of all fees applied to this transaction.

Format: `double`

string

The type of the investment transaction. Possible values are:

`buy`: Buying an investment

`sell`: Selling an investment

`cash`: Activity that modifies a cash position

`fee`: A fee on the account

`transfer`: Activity that modifies a position, but not through buy/sell activity e.g. options exercise, portfolio transfer

string

Either a valid `iso_currency_code` or `unofficial_currency_code`

object

Specify the security associated with the holding or investment transaction. When inputting custom security data to the Sandbox, Plaid will perform post-data-retrieval normalization and enrichment. These processes may cause the data returned by the Sandbox to be slightly different from the data you input. An ISO-4217 currency code and a security identifier (`ticker_symbol`, `cusip`, or `isin`) are required.

string

12-character ISIN, a globally unique securities identifier. A verified CUSIP Global Services license is required to receive this data. This field will be null by default for new customers, and null for existing customers starting March 12, 2024. If you would like access to this field, please [request ISIN/CUSIP access here](https://docs.google.com/forms/d/e/1FAIpQLSd9asHEYEfmf8fxJTHZTAfAzW4dugsnSu-HS2J51f1mxwd6Sw/viewform) .

string

9-character CUSIP, an identifier assigned to North American securities. A verified CUSIP Global Services license is required to receive this data. This field will be null by default for new customers, and null for existing customers starting March 12, 2024. If you would like access to this field, please [request ISIN/CUSIP access here](https://docs.google.com/forms/d/e/1FAIpQLSd9asHEYEfmf8fxJTHZTAfAzW4dugsnSu-HS2J51f1mxwd6Sw/viewform) .

string

A descriptive name for the security, suitable for display.

string

The security's trading symbol for publicly traded securities, and otherwise a short identifier if available.

string

Either a valid `iso_currency_code` or `unofficial_currency_code`

object

Data about the owner or owners of an account. Any fields not specified will be filled in with default Sandbox information.

\[string\]

A list of names associated with the account by the financial institution. These should always be the names of individuals, even for business accounts. Note that the same name data will be used for all accounts associated with an Item.

\[object\]

A list of phone numbers associated with the account.

string

The phone number.

boolean

When `true`, identifies the phone number as the primary number on an account.

string

The type of phone number.

Possible values: `home`, `work`, `office`, `mobile`, `mobile1`, `other`

\[object\]

A list of email addresses associated with the account.

string

The email address.

boolean

When `true`, identifies the email address as the primary email on an account.

string

The type of email account as described by the financial institution.

Possible values: `primary`, `secondary`, `other`

\[object\]

Data about the various addresses associated with the account.

object

Data about the components comprising an address.

string

The full city name

string

The region or state. Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

The postal code.

string

The ISO 3166-1 alpha-2 country code

boolean

When `true`, identifies the address as the primary address on an account.

object

Used to configure Sandbox test data for the Liabilities product

string

The type of the liability object: `credit` for a credit card, `student` for a student loan, `loan` for a closed-end loan, or `line_of_credit` for a line of credit. Mortgages are not currently supported in the custom Sandbox.

Possible values: `credit`, `student`, `loan`, `line_of_credit`

number

The purchase APR percentage value, between 0 and 100. For simplicity, this is the only interest rate used to calculate interest charges. Can only be set if `type` is `credit`.

Format: `double`

Minimum: `0`

Maximum: `100`

number

The cash APR percentage value, between 0 and 100. Can only be set if `type` is `credit`.

Format: `double`

Minimum: `0`

Maximum: `100`

number

The balance transfer APR percentage value, between 0 and 100. Can only be set if `type` is `credit`.

Format: `double`

Minimum: `0`

Maximum: `100`

number

The special APR percentage value, between 0 and 100. Can only be set if `type` is `credit`.

Format: `double`

Minimum: `0`

Maximum: `100`

number

Override the `last_payment_amount` field. Can only be set if `type` is `credit`, `loan`, or `line_of_credit`.

Format: `double`

number

Override the `last_statement_balance` field. Can only be set if `type` is `credit` or `line_of_credit`.

Format: `double`

number

Override the `minimum_payment_amount` field. Can only be set if `type` is `credit`, `student`, or `line_of_credit`.

Format: `double`

boolean

Override the `is_overdue` field. Can only be set if `type` is `credit` or `student`.

string

The date on which the loan was initially lent, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `student` or `loan`.

Format: `date`

number

The original loan principal. Can only be set if `type` is `student`.

Format: `double`

number

The interest rate on the loan as a percentage, between 0 and 100. Can only be set if `type` is `student`.

Format: `double`

Minimum: `0`

Maximum: `100`

integer

If set, interest capitalization begins at the given number of months after loan origination. By default interest is never capitalized. Can only be set if `type` is `student`.

Minimum: `0`

object

Student loan repayment information used to configure Sandbox test data for the Liabilities product

string

The only currently supported value for this field is `standard`.

number

Configures the number of months before repayment starts.

number

Configures the number of months of repayments before the loan is paid off.

string

Override the `expected_payoff_date` field. Can only be set if `type` is `student`.

Format: `date`

string

Override the `guarantor` field. Can only be set if `type` is `student`.

boolean

Override the `is_federal` field. Can only be set if `type` is `student`.

string

Override the `loan_name` field. Can only be set if `type` is `student`.

object

An object representing the status of the student loan

string

The date until which the loan will be in its current status. Dates are returned in an [ISO 8601](https://wikipedia.org/wiki/ISO_8601) format (YYYY-MM-DD).

Format: `date`

string

The status type of the student loan

Possible values: `cancelled`, `charged off`, `claim`, `consolidated`, `deferment`, `delinquent`, `discharged`, `extension`, `forbearance`, `in grace`, `in military`, `in school`, `not fully disbursed`, `other`, `paid in full`, `refunded`, `repayment`, `transferred`, `pending idr`

string

Override the `payment_reference_number` field. Can only be set if `type` is `student`.

string

Override the `repayment_plan.description` field. Can only be set if `type` is `student`.

string

Override the `repayment_plan.type` field. Can only be set if `type` is `student`. Possible values are: `"extended graduated"`, `"extended standard"`, `"graduated"`, `"income-contingent repayment"`, `"income-based repayment"`, `"income-sensitive repayment"`, `"interest only"`, `"other"`, `"pay as you earn"`, `"revised pay as you earn"`, `"standard"`, or `"saving on a valuable education"`.

number

Override the `sequence_number` field. Can only be set if `type` is `student`.

object

Data about the components comprising an address.

string

The full city name

string

The region or state. Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

The postal code.

string

The ISO 3166-1 alpha-2 country code

string

Override the `account_number` field. Can only be set if `type` is `loan`.

object

Override the `interest_rate` field. Can only be set if `type` is `loan` or `line_of_credit`.

number

The interest rate percentage, between 0 and 100.

Format: `double`

Minimum: `0`

Maximum: `100`

string

The type of interest rate.

Possible values: `fixed`, `variable`

number

Override the `principal_balance` field. Can only be set if `type` is `loan` or `line_of_credit`.

Format: `double`

number

Override the `origination_principal_amount` field. Can only be set if `type` is `loan`.

Format: `double`

integer

Override the `loan_term_months` field with a non-negative whole number. Can only be set if `type` is `loan`.

Minimum: `0`

string

Override the `maturity_date` field, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `loan`.

Format: `date`

integer

Override the `payment_count` field with a non-negative whole number. Can only be set if `type` is `loan`.

Minimum: `0`

string

Override the `payment_frequency` field. Can only be set if `type` is `loan`.

Possible values: `daily`, `weekly`, `biweekly`, `semimonthly`, `monthly`, `semiannually`, `annually`

number

Override the `next_payment_amount` field. Can only be set if `type` is `loan` or `line_of_credit`.

Format: `double`

string

Override the `next_payment_due_date` field, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `loan` or `line_of_credit`.

Format: `date`

string

Override the `last_payment_date` field, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `loan` or `line_of_credit`.

Format: `date`

number

Override the `payoff_amount` field. Can only be set if `type` is `loan`.

Format: `double`

number

Override the `ytd_interest_paid` field. Can only be set if `type` is `loan`.

Format: `double`

string

Override the `compounding_period` field. Can only be set if `type` is `loan`.

Possible values: `daily`, `weekly`, `biweekly`, `semimonthly`, `monthly`, `semiannually`, `annually`

number

Override the `credit_limit` field. Can only be set if `type` is `line_of_credit`.

Format: `double`

number

Override the `available_credit` field. Can only be set if `type` is `line_of_credit`.

Format: `double`

string

Override the `last_statement_issue_date` field, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `line_of_credit`.

Format: `date`

number

Override the `past_due_amount` field. Can only be set if `type` is `line_of_credit`.

Format: `double`

number

Override the `finance_charges` field. Can only be set if `type` is `line_of_credit`.

Format: `double`

string

Override the `draw_period_end_date` field, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD) format. Can only be set if `type` is `line_of_credit`.

Format: `date`

\[object\]

Override the `aprs` field. Can only be set if `type` is `line_of_credit`.

string

The type of balance to which the APR applies.

Possible values: `balance_transfer_apr`, `cash_apr`, `penalty_apr`, `purchase_apr`, `special`

number

The Annual Percentage Rate applied, between 0 and 100.

Format: `double`

Minimum: `0`

Maximum: `100`

number

Amount of money that is subjected to the APR if a balance was carried beyond payment due date.

Format: `double`

number

Amount of money charged due to interest from last statement.

Format: `double`

object

The `inflow_model` allows you to model a test account that receives regular income or makes regular payments on a loan. Any transactions generated by the `inflow_model` will appear in addition to randomly generated test data or transactions specified by `override_accounts`.

string

Inflow model. One of the following:

`none`: No income

`monthly-income`: Income occurs once per month

`monthly-balance-payment`: Pays off the balance on a liability account at the given statement day of month.

`monthly-interest-only-payment`: Makes an interest-only payment on a liability account at the given statement day of month.

Note that account types supported by Liabilities will accrue interest in the Sandbox. The types impacted are account type `credit` with subtype `credit` or `paypal`, and account type `loan` with subtype `student` or `mortgage`.

number

Amount of income per month. This value is required if `type` is `monthly-income`.

Format: `double`

Either a whole number between 1 and 28 or the string `last`, meaning the last day of the month. The day of the month on which the income transaction will appear. This field is required if `type` is `monthly-income`, `monthly-balance-payment` or `monthly-interest-only-payment`.

string

The name of the income transaction. This field is required if `type` is `monthly-income`, `monthly-balance-payment` or `monthly-interest-only-payment`.

Either a whole number between 1 and 28 or the string `last`, meaning the last day of the month. The day of the month on which the balance is calculated for the next payment. This field is required if `type` is `monthly-balance-payment` or `monthly-interest-only-payment`.

object

Specify payroll data on the account.

\[object\]

A list of paystubs associated with the account.

object

The employer on the paystub.

string

The name of the employer.

object

The address of the employer.

string

The full city name.

string

The region or state Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

5 digit postal code.

string

The country of the address.

object

The employee on the paystub.

string

The name of the employee.

object

The address of the employee.

string

The full city name.

string

The region or state Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

5 digit postal code.

string

The country of the address.

string

Marital status of the employee - either `single` or `married`.

Possible values: `single`, `married`

object

Taxpayer ID of the individual receiving the paystub.

string

Type of ID, e.g. 'SSN'

string

ID mask; i.e. last 4 digits of the taxpayer ID

object

An object representing information about the net pay amount on the paystub.

string

Description of the net pay

string

The ISO-4217 currency code of the net pay.

number

The year-to-date amount of the net pay

Format: `double`

object

An object with the deduction information found on a paystub.

\[object\]

number

Raw amount of the deduction

Format: `double`

string

Description of the deduction line item

string

The ISO-4217 currency code of the line item.

number

The year-to-date amount of the deduction

Format: `double`

object

An object representing the total deductions for the pay period

number

Raw amount of the deduction

Format: `double`

string

The ISO-4217 currency code of the line item.

number

The year-to-date total amount of the deductions

Format: `double`

object

An object representing both a breakdown of earnings on a paystub and the total earnings.

\[object\]

string

Commonly used term to describe the earning line item.

Possible values: `BONUS`, `COMMISSION`, `OVERTIME`, `PAID TIME OFF`, `REGULAR PAY`, `VACATION`, `BASIC ALLOWANCE HOUSING`, `BASIC ALLOWANCE SUBSISTENCE`, `OTHER`, `null`

number

Raw amount of the earning line item.

Format: `double`

string

Description of the earning line item.

number

Number of hours applicable for this earning.

string

The ISO-4217 currency code of the line item.

number

Hourly rate applicable for this earning.

Format: `double`

number

The year-to-date amount of the line item.

Format: `double`

object

An object representing both the current pay period and year to date amount for an earning category.

number

Total number of hours worked for this pay period

string

The ISO-4217 currency code of the line item

number

The year-to-date amount for the total earnings

Format: `double`

object

Details about the pay period.

number

The amount of the paycheck.

Format: `double`

\[object\]

string

Name of the account for the given distribution.

string

The name of the bank that the payment is being deposited to.

number

The amount distributed to this account.

Format: `double`

string

The ISO-4217 currency code of the net pay. Always `null` if `unofficial_currency_code` is non-null.

string

The last 2-4 alphanumeric characters of an account's official account number.

string

Type of the account that the paystub was sent to (e.g. 'checking').

string

The pay period end date, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) format: "yyyy-mm-dd".

Format: `date`

number

Total earnings before tax/deductions.

Format: `double`

string

The date on which the paystub was issued, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) format ("yyyy-mm-dd").

Format: `date`

deprecated, string

The date on which the paystub was issued, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) format ("yyyy-mm-dd").

Format: `date`

string

The pay period start date, in [ISO 8601](https://wikipedia.org/wiki/ISO_8601) format: "yyyy-mm-dd".

Format: `date`

\[object\]

A list of w2s associated with the account.

object

The employer on the paystub.

string

The name of the employer.

object

The address of the employer.

string

The full city name.

string

The region or state Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

5 digit postal code.

string

The country of the address.

object

The employee on the paystub.

string

The name of the employee.

object

The address of the employee.

string

The full city name.

string

The region or state Example: `"NC"`

string

The full street address Example: `"564 Main Street, APT 15"`

string

5 digit postal code.

string

The country of the address.

string

Marital status of the employee - either `single` or `married`.

Possible values: `single`, `married`

object

Taxpayer ID of the individual receiving the paystub.

string

Type of ID, e.g. 'SSN'

string

ID mask; i.e. last 4 digits of the taxpayer ID

integer

The tax year of the W2 document.

string

An employer identification number or EIN.

number

Wages from tips and other compensation.

Format: `double`

number

Federal income tax withheld for the tax year.

Format: `double`

number

Wages from Social Security.

Format: `double`

number

Social Security tax withheld for the tax year.

Format: `double`

number

Wages and tips from medicare.

Format: `double`

number

Medicare tax withheld for the tax year.

Format: `double`

number

Tips from Social Security.

Format: `double`

number

Allocated tips.

Format: `double`

string

Contents from box 9 on the W2.

number

Dependent care benefits.

Format: `double`

number

Nonqualified plans.

Format: `double`

\[object\]

string

W2 Box 12 code.

number

W2 Box 12 amount.

Format: `double`

boolean

Statutory employee.

boolean

Retirement plan.

boolean

Third party sick pay.

string

Other.

\[object\]

string

State associated with the wage.

string

State identification number of the employer.

number

Wages and tips from the specified state.

Format: `double`

number

Income tax from the specified state.

Format: `double`

number

Wages and tips from the locality.

Format: `double`

number

Income tax from the locality.

Format: `double`

string

Name of the locality.

object

Specifies the multi-factor authentication settings to use with this test account

string

Possible values are `device`, `selections`, or `questions`.

If value is `device`, the MFA answer is `1234`.

If value is `selections`, the MFA answer is always the first option.

If value is `questions`, the MFA answer is `answer_<i>_<j>` for the j-th question in the i-th round, starting from 0. For example, the answer to the first question in the second round is `answer_1_0`.

number

Number of rounds of questions. Required if value of `type` is `questions`.

number

Number of questions per round. Required if value of `type` is `questions`. If value of type is `selections`, default value is 2.

number

Number of rounds of selections, used if `type` is `selections`. Defaults to 1.

number

Number of available answers per question, used if `type` is `selections`. Defaults to 2.

string

You may trigger a reCAPTCHA in Plaid Link in the Sandbox environment by using the recaptcha field. Possible values are `good` or `bad`. A value of `good` will result in successful Item creation and `bad` will result in a `RECAPTCHA_BAD` error to simulate a failed reCAPTCHA. Both values require the reCAPTCHA to be manually solved within Plaid Link.

string

An error code to force on Item creation. Possible values are:

`"INSTITUTION_NOT_RESPONDING"` `"INSTITUTION_NO_LONGER_SUPPORTED"` `"INVALID_CREDENTIALS"` `"INVALID_MFA"` `"ITEM_LOCKED"` `"ITEM_LOGIN_REQUIRED"` `"ITEM_NOT_SUPPORTED"` `"INVALID_LINK_TOKEN"` `"MFA_NOT_SUPPORTED"` `"NO_ACCOUNTS"` `"PLAID_ERROR"` `"USER_INPUT_TIMEOUT"` `"USER_SETUP_REQUIRED"`

Sample custom user configuration

```json
{
  "seed": "my-seed-string-3",
  "roll_dates_forward": true,
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "identity": {
        "names": [
          "John Doe"
        ],
        "phone_numbers": [
          {
            "primary": true,
            "type": "home",
            "data": "4673956022"
          }
        ],
        "emails": [
          {
            "primary": true,
            "type": "primary",
            "data": "accountholder0@example.com"
          }
        ],
        "addresses": [
          {
            "primary": true,
            "data": {
              "city": "Malakoff",
              "region": "NY",
              "street": "2992 Cameron Road",
              "postal_code": "14236",
              "country": "US"
            }
          }
        ]
      },
      "transactions": [
        {
          "date_transacted": "2023-10-01",
          "date_posted": "2023-10-03",
          "currency": "USD",
          "amount": 100,
          "description": "1 year Netflix subscription"
        },
        {
          "date_transacted": "2023-10-01",
          "date_posted": "2023-10-02",
          "currency": "USD",
          "amount": 100,
          "description": "1 year mobile subscription"
        }
      ]
    },
    {
      "type": "loan",
      "subtype": "student",
      "liability": {
        "type": "student",
        "origination_date": "2023-01-01",
        "principal": 10000,
        "nominal_apr": 6.25,
        "loan_name": "Plaid Student Loan",
        "repayment_model": {
          "type": "standard",
          "non_repayment_months": 12,
          "repayment_months": 120
        }
      }
    },
    {
      "type": "credit",
      "subtype": "credit card",
      "starting_balance": 10000,
      "inflow_model": {
        "type": "monthly-interest-only-payment",
        "payment_day_of_month": 15,
        "statement_day_of_month": 13,
        "transaction_name": "Interest Payment"
      },
      "liability": {
        "type": "credit",
        "purchase_apr": 12.9,
        "balance_transfer_apr": 15.24,
        "cash_apr": 28.45,
        "special_apr": 0,
        "last_payment_amount": 500,
        "minimum_payment_amount": 10
      }
    },
    {
      "type": "investment",
      "subtype": "brokerage",
      "investment_transactions": [
        {
          "date": "2023-07-01",
          "name": "buy stock",
          "quantity": 10,
          "price": 10,
          "fees": 20,
          "type": "buy",
          "currency": "USD",
          "security": {
            "ticker_symbol": "PLAID",
            "currency": "USD"
          }
        }
      ],
      "holdings": [
        {
          "institution_price": 10,
          "institution_price_as_of": "2023-08-01",
          "cost_basis": 10,
          "quantity": 10,
          "currency": "USD",
          "security": {
            "ticker_symbol": "PLAID",
            "currency": "USD"
          }
        }
      ]
    },
    {
      "type": "payroll",
      "subtype": "payroll",
      "income": {
        "paystubs": [
          {
            "employer": {
              "name": "Heartland Toy Company"
            },
            "employee": {
              "name": "Chip Hazard",
              "address": {
                "city": "Burbank",
                "region": "CA",
                "street": "411 N Hollywood Way",
                "postal_code": "91505",
                "country": "US"
              }
            },
            "earnings": {
              "breakdown": [
                {
                  "canonical_description": "REGULAR PAY",
                  "description": "Regular",
                  "current_amount": 800,
                  "rate": 20,
                  "hours": 40
                },
                {
                  "canonical_description": "OVERTIME",
                  "description": "Overtime",
                  "current_amount": 200.39,
                  "rate": 30,
                  "hours": 6.68
                }
              ]
            },
            "pay_period_details": {
              "start_date": "2021-05-04",
              "end_date": "2021-05-18",
              "gross_earnings": 1000.39,
              "check_amount": 499.28
            }
          }
        ]
      }
    }
  ]
}
```