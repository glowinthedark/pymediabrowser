URL_TRANSFORMATIONS = [
    // LINK REGEX                                        MATCHING LINK REPLACEMENT
    // chineselearningonline.com
    [/clo_(\d{3}).*pdf/i,                                "../Audio/ChineseLearnOnline_$1.mp3"],
    // chinesepod content links (pdf, html)
    [/(.*chinesepod.*?)(?:_ex)?\.(pdf|html?)/i,          "../$1pr.aac"],
    // chinesepod media links (aac, mp3..)
    [/(.*chinesepod.*?)(?:(dg|pr|rv))?\.(aac|mp3|m4a)/i, "pdf/$1.pdf"]
];
