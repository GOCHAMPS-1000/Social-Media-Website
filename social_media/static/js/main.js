// Main JavaScript file for social media functionality
document.addEventListener('DOMContentLoaded', function() {
    // Like functionality
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            likePost(postId, this);
        });
    });

    // Comment functionality
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const commentInput = this.querySelector('.comment-input');
            const commentText = commentInput.value.trim();
            
            if (commentText) {
                addComment(postId, commentText, this);
                commentInput.value = '';
            }
        });
    });

    // Follow functionality
    document.querySelectorAll('.follow-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = this.dataset.username;
            const isFollowing = this.dataset.following === 'true';
            
            if (isFollowing) {
                unfollowUser(username, this);
            } else {
                followUser(username, this);
            }
        });
    });

    // Mark notification as read
    document.querySelectorAll('.mark-read-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const notificationId = this.dataset.notificationId;
            markAsRead(notificationId, this);
        });
    });
});

// AJAX function to like a post
function likePost(postId, formElement) {
    fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.liked) {
            formElement.classList.add('liked');
            formElement.querySelector('.like-btn').textContent = 'Unlike';
        } else {
            formElement.classList.remove('liked');
            form.querySelector('.like-btn').textContent = 'Like';
        }
        
        // Update like count
        const likeCountElement = formElement.querySelector('.like-count');
        if (likeCountElement) {
            likeCountElement.textContent = data.like_count;
        }
    })
    .catch(error => console.error('Error:', error));
}

// AJAX function to add a comment
function addComment(postId, commentText, formElement) {
    const formData = new FormData();
    formData.append('content', commentText);
    
    fetch(`/comment/${postId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const commentsList = formElement.closest('.post').querySelector('.comments-list');
            const newComment = document.createElement('li');
            newComment.innerHTML = `
                <strong>${data.comment.user}</strong>: ${data.comment.content}
                <small>${data.comment.created_at}</small>
            `;
            commentsList.appendChild(newComment);
        }
    })
    .catch(error => console.error('Error:', error));
}

// AJAX function to follow a user
function followUser(username, formElement) {
    fetch(`/follow/${username}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.following) {
            formElement.dataset.following = 'true';
            formElement.querySelector('.follow-btn').textContent = 'Unfollow';
            
            // Update follower count
            const followerCountElement = document.querySelector('.follower-count');
            if (followerCountElement) {
                followerCountElement.textContent = data.follower_count;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// AJAX function to unfollow a user
function unfollowUser(username, formElement) {
    fetch(`/unfollow/${username}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (!data.following) {
            formElement.dataset.following = 'false';
            formElement.querySelector('.follow-btn').textContent = 'Follow';
            
            // Update follower count
            const followerCountElement = document.querySelector('.follower-count');
            if (followerCountElement) {
                followerCountElement.textContent = data.follower_count;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// AJAX function to mark notification as read
function markAsRead(notificationId, btnElement) {
    fetch(`/notifications/mark/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const notificationItem = btnElement.closest('li');
            notificationItem.style.fontWeight = 'normal';
            btnElement.style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}