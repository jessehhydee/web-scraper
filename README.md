# web-scraper

A script that will scrape any url provided for the data requested.
The output is returned in JSON and formatted in the same way the input JSON is formatted.

## Rules for `input.json`
<ul>
<li>All dict objects must contain a url key/value.</li>
<li>Values to contain soup.select() selectors.</li>
<li>
If you require anything greater than the first instance of a selector, values to be a list.
<br>
The first value is the selector, and the second is the x instance of the selector
</li>
<li>Values not to contain an underscore character('_')</li>
</ul>

## Arguments

Script takes one argument of type boolean: `discard_url_in_output`
<br>
This is set to true by default.
<br><br>
If true, `url` is discarded from the output json
<br>
If false, `url` is kept in the output json