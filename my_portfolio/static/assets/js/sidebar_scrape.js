$.get("{% url 'blog:post_list' %}")
    .done(function(data) {
        let parser = new DOMParser();
        let doc = parser.parseFromString(data, "text/html");
        let element = doc.getElementsByClassName("col-md-4");
        appendText(element[0].innerHTML);
        console.log(element[0].innerHTML);
        function appendText (text) {
            let element = document.getElementById("scrape_get")
            element.insertAdjacentHTML("afterbegin", text ) ;
        };
    })