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
.bd-sidebar-secondary {
    max-width: none;
    flex: 0 0 28%;
    resize: horizontal;
    overflow: hidden;
    min-width: 150px;
    direction: rtl;
    border-left: 1px solid #d0d0d0;
}

.bd-sidebar-secondary > * {
    direction: ltr;
    overflow-y: auto;
    max-height: 100vh;
}

.bd-toc {
    width: 100%;
}

/* Decrease the width of the navigation sidebar */
.bd-sidebar-primary {
    flex: 0 0 20%;
    max-width: 25%;
    font-size: 0.85rem;
}

'''