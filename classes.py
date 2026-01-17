import tkinter as tk
class Ahead_btn:
    def __init__(self, root, edit_or_del, kotra_table):
        self.root = root
        self.edit_or_del = edit_or_del
        self.kotra_table = kotra_table
        self.create_knopky() 
        
    def create_knopky(self):
        self.mybutton = tk.Button(self.root, text="Вперед", command=self.kotry_diu_vukonatu)
        self.mybutton.pack(pady=20)

    def spusok_stovpciv_intable(self.kotra_table): 

    def kotry_diu_vukonatu(self):
        if self.edit_or_del == 'enter':
            stovpci = spusok_stovpciv_intable(self.kotra_table)
            for i in range(len(stovpci)):
               label = tk.Label(self.root, text=stovpci[i+1]) #f"Поле для ввода {i+1}:")
               label.pack(pady=(10, 0)) # Отступ сверху
               entry = tk.Entry(self.root)
               entry.pack(pady=5)
            print("Кнопка нажата")
            self.dissable_button()

            # data = insert_data_into_db()
        #elif  edit_or_del == 'del': 
        #    data = delete_data_from_db()  
        #else: 
        #    data = edit_data_in_db() 
        
    def dissable_button(self):    
        self.mybutton.config(state=tk.DISABLED)