/*

JQuery AJAX Search Functionality

Author: David Maxwell
Date: 2013-11-03
Revision: 2

*/

var stopHashChange = false;

$(function() {

    /*
    Returns the last word (or partial word) in the input box string.
    This word-in-progress is then sent to the server to provide suggestions as the user types their query.
     */
    function getSuggestion(object, term) {
        var element = $(object[0].element[0]);
        var current = element.val().split(' ');
        var old = element.data('oldVal').split(' ');

        // Update the oldVal data AFTER, not BEFORE.


        //return (""+term).replace(/[\s-]+$/,'').split(/[\s-]/).pop();
        return getDifferentTerm(old, current);
    }

    /*
    Removes the last (presumably incomplete) word from the given string and returns the spliced string.
    From this shortened string, we can then add our complete suggestion to the query string.
     */
    function removeSuggestionText(inputString) {
        var lastSpaceIndex = inputString.lastIndexOf(" ");
        return inputString.substring(0, lastSpaceIndex);
    }

    /*
    Bind all input fields to have autocomplete functionality.
    Check out http://api.jquery.com/text-selector/ for more information on the selector used.
     */
    $(':text').autocomplete({
        minLength: 2,
        source: function( request, response ) {

        $.ajax({
            url: "",
            dataType: "json",
            data: {
                suggest: getSuggestion($(this), request.term)[0]
            },
            success: function(data) {
            response( $.map( data.results, function(item) {
                return {
                    label: item,
                    value: item}
                }));
            }});
        },
        focus: function(event) {
            event.preventDefault();

        },
        select: function(event, ui) {
            event.preventDefault();
            var currFieldValue = event.target.value;
            var previousValue = $(this).data('oldVal');

            var selectedItem = ui.item.value;
            var newFieldValue = "";

            oldArray = previousValue.split(' ');
            newArray = currFieldValue.split(' ');

            var difference = getDifferentTerm(oldArray, newArray);



            if (previousValue === undefined) {
                newFieldValue = selectedItem
            }
            else {
                for (termIndex in newArray) {
                    if (termIndex == difference[1]) {
                        if (termIndex == 0) newFieldValue += selectedItem;
                        else newFieldValue += " " + selectedItem;
                    }
                    else {
                        if (termIndex == 0) newFieldValue += newArray[termIndex];
                        else newFieldValue += " " + newArray[termIndex];
                    }
                }
            }

            event.target.value = newFieldValue;
            $(this).data('oldVal', $(this).val());
      }
    });

    // When the search form is submitted...
    $("#search_form").submit(function(event) {
        event.preventDefault();
        processRequest($("form").serialize());
    });

    $(document).ready(function() {
        $(':text').each(function(i, obj) {
            var element = $(obj);
            element.data('oldVal', element.val());
        });
    });

    // When the URL hash changes, check the data and see if a search can be performed.
    $(window).hashchange(function() {
        if (!stopHashChange)
            doHashSearch();

        stopHashChange = false;
    });

    $(window).hashchange();
});

/*
A function which returns the term that appears within two arrays differently.
This is used to determine which word to focus on in the suggestion box.
An array is returned, containing the differing term at [0] and the position of the word (zero-based) at [1].
*/
function getDifferentTerm(oldArray, newArray) {
    var returnArray = [];
    var i = 0;

    jQuery.grep(newArray, function(element) {
        if (jQuery.inArray(element, oldArray) == -1) {
            returnArray = [element, i];
        }

        i++;
    });

    return returnArray;
}

/*
Switches the current search results to the page specified by the URL supplied.
*/
function switchToPage(url) {
    var pageNumber = getPageNumber(url);
    var formData = $("form").serialize();
    formData = formData + '&page=' + pageNumber;

    processRequest(formData);
}

/*
Returns the page number that has been requested from the given URL.
*/
function getPageNumber(url) {
    if (url.substring(0, 1) == '?') {
        url = url.substring(1, url.length);
    }

    var vars = url.split('&');

    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');

        if (pair[0] == 'page') {
            return parseInt(pair[1]);
        }
    }

    return false;
}

/*
The URL hash (everything after the #, including the #) is being used in a querystring-style format.
Specify a key as the parameter for this function and you'll get the corresponding value.
With a hash of #query=bbc&page=2, getHashValue('query') returns 'bbc'.

Solution adapted from http://stackoverflow.com/a/3788235.
*/
function getHashValue(key) {
    var re = new RegExp('(?:\\#|&)'+key+'=(.*?)(?=&|$)','gi');
    var r = [];
    var m;

    while ((m = re.exec(document.location.hash)) != null) {
        r.push(m[1]);
    }

    if(typeof(r[0]) === 'undefined') {
        return false;
    }

    return r[0];
}

/*
Function which processes the AJAX request. Sends the request and displays the results on the page.
*/
function processRequest(serializedFormData) {
    $('body').css('cursor', 'progress');
    var posting = $.post("", serializedFormData);

    posting.fail(function(data) {
        $('body').css('cursor', 'default');
        alert("Something went wrong when processing your request!");
        console.log("Server error on AJAX request: " + data.responseText);
    });

    posting.done(function(data) {
        var results = $('div.results');
        results.empty(); // Remove all children for the new results set

        var results_nav = $('div.results_nav');
        results_nav.empty(); // Remove all children from the navigation button container

        if ('timeout' in data) {
            results.append('<div class="query" style="text-align: center;"><strong>Task Timed Out.</strong><br />Your search task has timed out. Please click <a href="/treconomics/next/">here</a> to continue.</div>');
        }
        else {
            if (data['trec_search']) {
                // Add the top part
                results.append('<div class="query"><strong>Search Terms: <em>' + data['query'] + '</em></strong> <span>Showing page <em>' + data['curr_page'] + '</em> out of <em>' + data['num_pages'] + '</em> page(s).</span></div>');

                // Add each of the results
                for (var result_no in data['trec_results']) {
                    var result = data['trec_results'][result_no];
                    results.append('<div class="entry" id="' + result['docid'] + '"><p class="result_title"><a href="' + result['url'] + '"><strong>' + result['title'] + '</strong></a></p><p class="summary">' + result['summary'] + '</p></div>');
                    results.append('<div class="byline">' + result['source'] + '</div>');
                }

                // Add navigation buttons at bottom of page (if applicable)
                var nextButton = "";
                var prevButton = "";

                if (data['curr_page'] < data['num_pages']) {
                    nextButton = '<input class="largebutton" type="button" onclick="switchToPage(\'' + data['next_page_link'] + '\');" value="Next Page" />';
                }

                if (data['curr_page'] > 1) {
                    prevButton = '<input class="largebutton" type="button" onclick="switchToPage(\'' + data['prev_page_link'] + '\');" value="Prev Page" />';
                }

                results_nav.append('<div class="result_nav"><center><form>' + prevButton + nextButton + '</form></center></div>');
            }
            else {
                results.append('<div class="query"><strong>Search Terms: <em>' + data['query'] + '</em></strong> <span>No results found.</span></div>');
            }

            stopHashChange = true;

            if ('curr_page' in data) {
                window.location.hash = 'query=' + data['query'] + '&page=' + data['curr_page'];
            }
            else {
                window.location.hash = 'query=' + data['query'];
            }
        }

        $('body').css('cursor', 'default');
    });
}

/*
Checks data supplied as part of the URL hash and performs a search if it is acceptable.
*/
function doHashSearch() {
    var query = getHashValue('query');
    var page = getHashValue('page');

    if (query) {
        if (!page || isNaN(page)) {
            page = 1;
        }

        if (/\S/.test(query)) {  // Check if string contains at least one non-whitespace character
            var queryField = $('#query');

            if (queryField && queryField.attr('name')) { // Is this interface 1?
                queryField.val(query);
                var formSerialized = $('form').serialize();
                formSerialized += '&page=' + page;

                processRequest(formSerialized);
            }
        }
    }
}