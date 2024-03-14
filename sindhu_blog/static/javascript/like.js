// Obtain CSRF token from cookie
function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    // Event listener for the "Like" button click
    $('#like_button').click(function() {
        var blogId = $(this).val(); // Get the blog post ID from the button value

        // Send an AJAX POST request to like the blog post
        $.ajax({
            url: '/like/' + blogId + '/',
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                if (response.error === 'You have already liked this post') {
                    $('#error-message').text(response.error);
                } else {
                    // Update the likes count on the webpage
                    $('#like-count').text(response.likes);
                    $('#dislike-count').text(response.dislikes);
                }
            },
            error: function(xhr, status, error) {
                alert('You have already liked this post');
            }
        });
    });

    // Event listener for the "Dislike" button click
    $('#dislike_button').click(function() {
        var blogId = $(this).val(); // Get the blog post ID from the button value

        // Send an AJAX POST request to like the blog post
        $.ajax({
            url: '/dislike/' + blogId + '/',
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                if (response.error === 'You have already disliked this post')
                {
                    $('#error-message').text(response.error);                }
                else
                {
                    $('#like-count').text(response.likes);
                    $('#dislike-count').text(response.dislikes);
                }
            },
            error: function(xhr, status, error) {
                alert('You have already disliked this post');
            }
        });
    });
    $('#comment-form').submit(function(e) {
                e.preventDefault();  // Prevent default form submission
                var blogId = $('#comment-form input[name="blog_id"]').val();
                var commentText = $('#comment-content').val();
                console.log(commentText)
                console.log(blogId)
                $.ajax({
                    url: '/comment/' + blogId + '/',  // URL to the view handling form submission
                    type: 'POST',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },
                    data: {'blog_id': blogId,
                            'comment_text': commentText},
                    success: function(response)
                    {
                        if (response.success)
                        {
                            var newComment = '<div><strong>' + response.username + ' - ' + response.date +'</strong><br> ' + response.content + '</div>';
                            $('#comment-list').append(newComment);
                            $('#comment-form')[0].reset();  // Reset the form
                        }
                        else
                        {
                            console.log(response.errors);
                        }
                    }
                });
    });
});
