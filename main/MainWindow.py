import tkinter as tk
from tkinter import ttk
from models.post import Post

from main.connection_requests_window import ConnectionRequestsWindow
from main.followed_list_window import FollowedListWindow
from main.profile_window import ProfileWindow
from main.company_profile_window import CompanyProfileWindow
from main.skill_window import SkillWindow
from main.job_list_window import JobListWindow
from main.job_post_window import JobPostWindow
from main.application_list_window import ApplicationListWindow
from main.incoming_applications_window import IncomingApplicationsWindow
from models.post_like import PostLike
from models.comment import Comment


class MainWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.title("Professional Skill Network - Main Page")
        self.geometry("1100x600")
        self.configure(bg="#f4f4f4")
        self.user = user

        # Sol buton paneli
        sidebar = tk.Frame(self, bg="#f4f4f4", width=250)
        sidebar.pack(side="left", fill="y")

        greeting = f"Welcome, {user.fullName} ({user.role})"
        tk.Label(sidebar, text=greeting, font=("Segoe UI", 14, "bold"),
                 bg="#f4f4f4", fg="#0D4D56").pack(pady=20)

        ttk.Button(sidebar, text="👤 View Profile", command=self.view_profile).pack(pady=5, fill="x", padx=20)

        if self.user.role == "individual":
            ttk.Button(sidebar, text="🧠 Skills", command=self.view_skills).pack(pady=5, fill="x", padx=20)

        ttk.Button(sidebar, text="🌐 Discover People", command=self.open_social_window).pack(pady=5, fill="x", padx=20)
        ttk.Button(sidebar, text="🔗 Connection Requests", command=self.view_connection_requests).pack(pady=5, fill="x", padx=20)
        ttk.Button(sidebar, text="👁️ Followers", command=self.view_followers).pack(pady=5, fill="x", padx=20)
        ttk.Button(sidebar, text="🤝 Connections", command=self.view_connections).pack(pady=5, fill="x", padx=20)
        ttk.Button(sidebar, text="👥 Followed Users", command=self.view_followed_users).pack(pady=5, fill="x", padx=20)

        if self.user.role == "individual":
            ttk.Button(sidebar, text="🔍 Find Jobs", command=self.find_jobs).pack(pady=5, fill="x", padx=20)
            ttk.Button(sidebar, text="📄 My Applications", command=self.view_my_applications).pack(pady=5, fill="x", padx=20)

        elif self.user.role == "company":
            ttk.Button(sidebar, text="📢 Post a Job", command=self.post_job).pack(pady=5, fill="x", padx=20)
            ttk.Button(sidebar, text="📨 View Applications", command=self.view_incoming_applications).pack(pady=5, fill="x", padx=20)

        ttk.Button(sidebar, text="🚪 Logout", command=self.logout).pack(pady=20, fill="x", padx=20)

        # Sağ feed alanı
        self.create_feed_section()

    def create_feed_section(self):
        self.feed_frame = tk.Frame(self, bg="white")
        self.feed_frame.pack(side="right", fill="both", expand=True)

        tk.Label(self.feed_frame, text="📢 Share an update", font=("Segoe UI", 14, "bold"),
                 bg="white").pack(pady=10)

        self.post_text = tk.Text(self.feed_frame, height=3, wrap="word")
        self.post_text.pack(padx=20, fill="x")

        ttk.Button(self.feed_frame, text="📤 Share", command=self.share_post).pack(pady=5)

        ttk.Separator(self.feed_frame).pack(fill="x", pady=5)

        # Scrollable post listesi
        self.feed_canvas = tk.Canvas(self.feed_frame, bg="white", highlightthickness=0)
        self.feed_scrollbar = ttk.Scrollbar(self.feed_frame, orient="vertical", command=self.feed_canvas.yview)
        self.feed_canvas.configure(yscrollcommand=self.feed_scrollbar.set)

        self.feed_inner = tk.Frame(self.feed_canvas, bg="white")
        self.feed_canvas.create_window((0, 0), window=self.feed_inner, anchor="nw")

        self.feed_inner.bind("<Configure>", lambda e: self.feed_canvas.configure(scrollregion=self.feed_canvas.bbox("all")))

        self.feed_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        self.feed_scrollbar.pack(side="right", fill="y")

        self.load_feed_posts()

    def share_post(self):
        content = self.post_text.get("1.0", "end").strip()
        if content:
            post = Post(user_id=self.user.id, content=content)
            post.save()
            self.post_text.delete("1.0", "end")
            self.load_feed_posts()

    def load_feed_posts(self):
        for widget in self.feed_inner.winfo_children():
            widget.destroy()

        posts = Post.get_all_for_feed(self.user.id)
        for post_id, author, content, created_at in posts:
            post_frame = tk.Frame(self.feed_inner, bg="#f9f9f9", pady=5, padx=10, bd=1, relief="solid")
            post_frame.pack(fill="x", pady=5, padx=10)

            # Gönderi başlığı
            tk.Label(post_frame, text=author, font=("Segoe UI", 10, "bold"), bg="#f9f9f9").pack(anchor="w")
            tk.Label(post_frame, text=created_at.strftime("%Y-%m-%d %H:%M"), font=("Segoe UI", 8), bg="#f9f9f9").pack(
                anchor="w")
            tk.Label(post_frame, text=content, wraplength=500, justify="left", bg="#f9f9f9").pack(anchor="w", pady=5)

            # Beğeni sayısı
            like_count = PostLike.count_likes(post_id)
            like_label = tk.Label(post_frame, text=f"❤️ {like_count} likes", font=("Segoe UI", 9), bg="#f9f9f9")
            like_label.pack(anchor="w", pady=(0, 2))

            # Beğen butonu
            def like_post(post_id=post_id):
                PostLike(self.user.id, post_id).save()
                self.load_feed_posts()

            ttk.Button(post_frame, text="👍 Like", command=like_post).pack(anchor="w", pady=(0, 5))

            # Yorumlar
            comments = Comment.get_comments(post_id)
            if comments:
                tk.Label(post_frame, text="💬 Comments:", font=("Segoe UI", 9, "bold"), bg="#f9f9f9").pack(anchor="w")
                for author_name, comment_text, comment_time in comments:
                    comment_str = f"• {author_name}: {comment_text}"
                    tk.Label(post_frame, text=comment_str, wraplength=450, justify="left", bg="#f9f9f9",
                             font=("Segoe UI", 9)).pack(anchor="w")

            # Yeni yorum ekleme
            comment_entry = tk.Entry(post_frame, width=60)
            comment_entry.pack(anchor="w", pady=5)

            def submit_comment(post_id=post_id, entry=comment_entry):
                text = entry.get().strip()
                if text:
                    Comment(post_id=post_id, user_id=self.user.id, text=text).save()
                    self.load_feed_posts()

            ttk.Button(post_frame, text="💬 Add Comment", command=submit_comment).pack(anchor="w", pady=(0, 10))

    def view_profile(self):
        if self.user.role == "company":
            CompanyProfileWindow(self.user.id)
        else:
            ProfileWindow(self.user.id)

    def view_skills(self):
        SkillWindow(self.user)

    def post_job(self):
        JobPostWindow(self.user)

    def find_jobs(self):
        JobListWindow(self.user)

    def view_applications(self):
        ApplicationListWindow(self.user)

    def open_social_window(self):
        from main.social_window import SocialWindow
        SocialWindow(self.user.id)

    def view_connection_requests(self):
        ConnectionRequestsWindow(self.user.id)

    def view_incoming_applications(self):
        from main.incoming_applications_window import IncomingApplicationsWindow
        IncomingApplicationsWindow(self.user)

    def view_my_applications(self):
        from main.my_applications_window import MyApplicationsWindow
        MyApplicationsWindow(user_id=self.user.id)

    def view_followed_users(self):
        FollowedListWindow(self.user.id)

    def view_followers(self):
        from main.follower_list_window import FollowerListWindow
        FollowerListWindow(self.user.id)

    def view_connections(self):
        from main.connection_list_window import ConnectionListWindow
        ConnectionListWindow(self.user)

    def logout(self):
        self.destroy()
