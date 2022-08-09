## Usage

You need to provide valid Stack Exchange credentials in the form of a `client_id`, `client_secret` and `key` by [creating a "Stack App"](https://stackapps.com/apps/oauth/register). These should be added to `credentials.json`.

Then:
- To download the profile and answer data for the list of users in `data/alltop100/users`, run `scrape_top.py` -- this downloads data in JSON format from the StackExchange API.
- To reformat the raw JSON responses, run `flatten_top.py`. This produces 'flat' CSV files `data/alltop100x100/users.csv` and `data/alltop100x100/answers.csv`. 
- To download all questions and answers from the Information Security Stack Exchange run `scrape_all.py`. This downloads data in JSON format.
- To reformat the JSON into CSV, run `flatten_all.py`. This produces CSV files `data/all/answers.csv` and `data/all/unanswered.csv`. Question data and metadata is included with each answer.
