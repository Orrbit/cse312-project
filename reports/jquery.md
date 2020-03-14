# jQuery - jQuery: "write less, do more"

jQuery is a JavaScript framework that "makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers" (https://jquery.com/). With
jQuery we can simplify the manipulation of UI elements. It is also a dependency for the BootStrap library to accomplish
its goals.

**jQuery Documentation** - (https://api.jquery.com/)

**Download jQuery Source Code** - (https://jquery.com/download/)

# Phase 1
For Phase 1, we have used jQuery in the file questions.js. This file is served with questions.html and assigns a handler
to the form used to add a comment to a thread so when you hit submit, your comment is added to the UI. This is the only instance
where we implement our own code and can be seen below:

```
$(document).ready(function(){
    $("#add-comment").submit(function(){
        let msg = $(this).find('textarea').val()
        let html = `<div class='my-comment bg-light text-dark'>
        <h4>Brian</h4>
        <p class='comment-content'>
            ${msg}
        </p>
        <div class='comment-footer'>
            <button class='btn btn-primary float-right mx-2'>
                <i class='fa fa-thumbs-up'></i>
                <span class='badge badge-light'>0</span>
            </button>
            <button class='btn btn-primary float-right mx-2'>
                <i class='fa fa-star'></i>
                <span class='badge badge-light'>0</span>
            </button>
        </div>
        </div>`
        $("#question-thread").append(html);
    });
});
```

There are script tags with references to the jQuery library in several of our html files however this is because BootStrap
makes use of this library. This is discussed further in BootStrap's documentation (https://getbootstrap.com/docs/4.4/getting-started/introduction/).

## What is jQuery accomplishing for our group?
jQuery aids in the manipulation of UI elements with our own JavaScript code and through the BootStrap library. It will also
simplify the AJAX request process. This will allow us to build front-end components quickly and correctly. In the above code
snippet, we see the syntax ```$(<CSS Selector>).someAction(...)```. The $ accesses the jQuery library and it will then find the elements with the associated selector and then perform the actions specified.
  
## How does jQuery accomplish its goals?
jQuery parses the Document Object Model (DOM) to find the elements that you specify and applies the provided actions. This is something that could be done with the native JavaScript library and replicated fairly easily. However, it is much easier to use the code that jQuery has implemented. 

## Is there any licensing?
Copyright JS Foundation and other contributors, https://js.foundation/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.