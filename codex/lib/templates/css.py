CUSTOM_CSS_TEMPLATE = '''\
/* Increase maximum page width */
.bd-page-width {
    max-width: 75%;
}

/* Allow the main content area to be wider */
.bd-main .bd-content .bd-article-container {
    max-width: none;
}

/* Increase the width of code blocks */
div.highlight, div.cell_input, pre {
    overflow: auto;
    max-width: 100%;
}

/* Increase the width of the right sidebar */
.bd-sidebar-right {
    max-width: 75%;
}

/* Decrease the width of the navigation sidebar */
.bd-sidebar-left {
    max-width: 10%;
}

'''