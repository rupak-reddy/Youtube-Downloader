import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import os
from jnius import autoclass, PythonJavaClass, java_method
import youtube_dl

class YoutubeVideoDownloader(toga.App):
    def download_video(self, widget):
        try:
            ytlink = self.url_input.value
            # Request permissions
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PackageManager = autoclass('android.content.pm.PackageManager')
            perm_read = autoclass('android.Manifest$permission').READ_EXTERNAL_STORAGE
            perm_write = autoclass('android.Manifest$permission').WRITE_EXTERNAL_STORAGE

            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()
            package_manager = context.getPackageManager()

            if (
                package_manager.checkPermission(perm_read, context) != PackageManager.PERMISSION_GRANTED
                or package_manager.checkPermission(perm_write, context) != PackageManager.PERMISSION_GRANTED
            ):
                # Permissions not granted, request them
                activity.requestPermissions([perm_read, perm_write], 1)
                return

            ydl_opts = {
                'outtmpl': os.path.join(os.environ['EXTERNAL_STORAGE'], 'YouTube', '%(title)s.%(ext)s'),
                'format': 'best',
                'progress_hooks': [self.on_progress],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(ytlink, download=True)

            self.status_label.text = "Video Downloaded Successfully to the YouTube Folder in your Phone"
            self.text1.text = "Name of the Video: " + info['title']
            self.text2.text = "Author: " + info['uploader']
            self.text3.text = "Channel URL: " + info['channel_url']
            duration = info.get('duration')
            if duration:
                duration_min = duration // 60
                duration_sec = duration % 60
                self.text4.text = f"Duration: {duration_min} minutes, {duration_sec} seconds"
            else:
                self.text4.text = ""
            self.text5.text = "Publish Date: " + info['upload_date']
            self.text6.text = "Number of Views: " + str(info.get('view_count', ''))
        except Exception as e:
            self.status_label.text = "The given YouTube link is invalid or it no longer exists."


    def on_progress(self, data):
        if data['status'] == 'downloading':
            percentage_of_completion = (data['downloaded_bytes'] / data['total_bytes']) * 100
            self.progress_label.text = f"Progress: {percentage_of_completion:.2f}%"
            self.progress_bar.value = percentage_of_completion

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, background_color="black"))

        name_label = toga.Label(
            "Welcome to YouTube Downloader",
            style=Pack(padding=(20, 50), color="yellow", text_align="center", font_size=20),
        )

        text = toga.Label("Type or Paste a Video URL : ", style=Pack(font_size=18, color="white", padding=(15, 0)))
        self.text1 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))
        self.text2 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))
        self.text3 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))
        self.text4 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))
        self.text5 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))
        self.text6 = toga.Label("", style=Pack(padding=(12, 0), font_size=15, color="white"))

        self.url_input = toga.TextInput(placeholder="Enter YouTube link", style=Pack(padding=(15, 0)))
        self.progress_label = toga.Label("Progress: ", style=Pack(font_size=18))
        self.progress_bar = toga.ProgressBar(max=100)
        self.status_label = toga.Label("")
        self.download_button = toga.Button(
            "Download", on_press=self.download_video, style=Pack(background_color="blue", padding=(15, 0))
        )

        main_box.add(name_label)
        main_box.add(text)
        main_box.add(self.url_input)
        main_box.add(self.progress_label)
        main_box.add(self.progress_bar)
        main_box.add(self.download_button)
        main_box.add(self.status_label)
        main_box.add(self.text1)
        main_box.add(self.text2)
        main_box.add(self.text3)
        main_box.add(self.text4)
        main_box.add(self.text5)
        main_box.add(self.text6)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return YoutubeVideoDownloader()
