import tkinter as tk
from PIL import Image, ImageTk
import folium
from folium.plugins import MarkerCluster
import webbrowser
import csv
import os

class FoodItem:
    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.image_path = image_path

class HalmaeTasteTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Halmae Taste Test")
        self.root.geometry("500x500")  # 창 크기를 500x500으로 고정
        self.score = 0

        self.questions = [
            FoodItem("콩떡", "콩설기를 좋아합니까?", "images/떡.png"),
            FoodItem("맛동산", "맛동산 과자를 좋아합니까?", "images/맛동산.png"),
            FoodItem("모나카", "모나카를 좋아합니까?", "images/모나카.png"),
            FoodItem("비비빅", "비비빅 아이스크림을 좋아합니까?", "images/비비빅.png"),
            FoodItem("뻥튀기", "뻥튀기를 좋아합니까?", "images/뻥튀기.png"),
            FoodItem("수정과", "수정과를 좋아합니까?", "images/수정과.png"),
            FoodItem("약과", "약과를 좋아합니까?", "images/약과.png"),
            FoodItem("연양갱", "양갱을 좋아합니까?", "images/연양갱.png"),
            FoodItem("유과", "유과를 좋아합니까?", "images/유과.png"),
            FoodItem("짱구", "못말리는 신짱 과자를 좋아합니까?", "images/짱구.png"),
            FoodItem("참쌀선과", "참쌀 과자를 좋아합니까?", "images/참쌀선과.png"),
            FoodItem("콩국수", "콩국수를 좋아합니까?", "images/콩국수.png"),
            FoodItem("팥단호박죽", "호박죽/팥죽을 좋아합니까?", "images/팥단호박죽.png")
        ]

        self.question_index = 0
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()
        start_label = tk.Label(self.root, text="할매입맛 테스트 시작 !")
        start_label.pack(pady=20)
        start_button = tk.Button(self.root, text="Start", command=self.start_test)
        start_button.pack(pady=10)

    def start_test(self):
        self.clear_screen()
        self.show_question()

    def show_question(self):
        if self.question_index < len(self.questions):
            food_item = self.questions[self.question_index]
            question_label = tk.Label(self.root, text=food_item.description)
            question_label.pack(pady=20)
            
            image = Image.open(food_item.image_path)
            image = image.resize((300, 300), Image.LANCZOS)  # 이미지를 300x300으로 리사이징
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.root, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)

            yes_button = tk.Button(self.root, text="Yes", command=self.answer_yes)
            yes_button.pack(side=tk.LEFT, padx=20, pady=10)
            no_button = tk.Button(self.root, text="No", command=self.answer_no)
            no_button.pack(side=tk.RIGHT, padx=20, pady=10)
        else:
            self.show_result()

    def answer_yes(self):
        self.score += 1
        self.question_index += 1
        self.clear_screen()
        self.show_question()

    def answer_no(self):
        self.question_index += 1
        self.clear_screen()
        self.show_question()

    def show_result(self):
        self.clear_screen()
        level = self.get_level()
        result_label = tk.Label(self.root, text=f"당신의 할매력은 Level {level}입니다.")
        result_label.pack(pady=20)
        recommend_button = tk.Button(self.root, text="할매력을 끌어올리기 위한 맛집 보기", command=self.show_recommendation)
        recommend_button.pack(pady=10)

    def get_level(self):
        if self.score <= 3:
            return 1
        elif self.score <= 8:
            return 2
        else:
            return 3

    def show_recommendation(self):
        level = self.get_level()
        restaurants = self.get_restaurants_by_level(level)
        self.create_map(restaurants)

    def get_restaurants_by_level(self, level):
        restaurants = []
        with open('restaurants.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['level']) == level:
                    restaurants.append({
                        "name": row['name'],
                        "location": (float(row['latitude']), float(row['longitude'])),
                        "menu": row['menu']
                    })
        return restaurants

    def create_map(self, restaurants):
        map_center = (35.888836, 128.6102997)
        halmae_map = folium.Map(location=map_center, zoom_start=12)
        marker_cluster = MarkerCluster().add_to(halmae_map)
        
        for restaurant in restaurants:
            folium.Marker(
                location=restaurant["location"],
                popup=f"{restaurant['name']} ({restaurant['menu']})",
                icon=folium.Icon(icon="cutlery", prefix="fa")
            ).add_to(marker_cluster)
        
        # 지도 저장
        map_file = "halmae_map.html"
        halmae_map.save(map_file)
        
        # 절대 경로로 파일을 열기
        abs_path = os.path.abspath(map_file)
        webbrowser.open('file://' + abs_path)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HalmaeTasteTestApp(root)
    root.mainloop()
