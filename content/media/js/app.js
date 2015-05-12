{% if site.config.mode == "production" %}
WebFontConfig = {
    google: { families: [ 'Open+Sans:400,400italic:latin', 'Source+Sans+Pro:900:latin' ] }
};
(function() {
    var wf = document.createElement('script');
    wf.src = ('https:' == document.location.protocol ? 'https' : 'http') +
        '://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
    wf.type = 'text/javascript';
    wf.async = 'true';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(wf, s);
})();

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', '{{ site.meta.ga_tracking_code }}', 'auto');
ga('send', 'pageview');
{% endif %}

(function() {
    /**
     * Utility to wrap the different behaviors between W3C-compliant browsers
     * and IE when adding event handlers.
     *
     * @param {Object} element Object on which to attach the event listener.
     * @param {string} type A string representing the event type to listen for
     *     (e.g. load, click, etc.).
     * @param {function()} callback The function that receives the notification.
     */
    function addListener(element, type, callback) {
        if (element.addEventListener) element.addEventListener(type, callback);
        else if (element.attachEvent) element.attachEvent('on' + type, callback);
    }

    function addAnalyticsEvent(element) {
        var eventObject = {};
        eventObject.hitType = "event";
        eventObject.eventCategory = element.dataset.gacategory;
        eventObject.eventAction = element.dataset.gaaction;
        if (element.dataset.galabel) {
            eventObject.eventLabel = element.dataset.galabel;
        }
        addListener(element, "click", function() {
            {% if site.config.mode == "production" -%}
            ga("send", eventObject);
            {%- else -%}
            console.log(eventObject);
            {%- endif %}
        });
    }

    var actionableElements = document.querySelectorAll("[data-action]");
    [].forEach.call(actionableElements, function(element, index, array) {
        switch (element.dataset.action) {
            case "track-event":
                addAnalyticsEvent(element);
                break;
        }
    });
})();
