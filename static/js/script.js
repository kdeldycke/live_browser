
            /**
             * Callback function that displays the content.
             *
             * Gets called every time the user clicks on a pagination link.
             *
             * @param {int} page_index New Page index
             * @param {jQuery} jq the container with the pagination links as a jQuery object
             */
            function pageselectCallback(page_index, jq){
                var new_content = jQuery('#hiddenresult div.result:eq('+page_index+')').clone();
                $('#Searchresult').empty().append(new_content);
                return false;
            }

            /** 
             * Initialisation function for pagination
             */
            function initPagination() {
                // count entries inside the hidden content
                var num_entries = jQuery('#hiddenresult div.result').length;
                // Create content inside pagination element
                $("#Pagination").pagination(num_entries, {
                    callback: pageselectCallback,
                    items_per_page:1 // Show only one item per page
                });
             }

            // When document is ready, initialize pagination
            $(function(){
                initPagination();
                $('#Pagination').trigger('setPage', [0]);
            });

