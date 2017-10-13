URL_TRANSFORMATIONS = [
    // LINK REGEX                                        REPLACE PREFIX              REPLACE SUFFIX
    // chineselearningonline.com
    [/clo_(\d{3}).*pdf/i,                                "../Audio/ChineseLearnOnline_",    ".mp3"],
    // chinesepod content links (pdf, html)
    [/(.*chinesepod.*)(?:_ex)?\.(pdf|html?)/i,           "../",                           "pr.aac"],
    // chinesepod media links (aac, mp3..)
    [/(.*chinesepod.*?)(?:(dg|pr|rv))?\.(aac|mp3|m4a)/i, "pdf/",                            ".pdf"]
];
