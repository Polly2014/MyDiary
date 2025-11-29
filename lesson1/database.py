"""
数据库管理模块
负责所有与SQLite数据库相关的操作
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "mydiary.db"):
        """
        初始化数据库管理器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库，创建表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建日记表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT DEFAULT 'neutral',
                created_date DATE NOT NULL,
                modified_date DATETIME,
                word_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成: {self.db_path}")
    
    def add_diary(self, title: str, content: str, mood: str = 'neutral') -> int:
        """
        添加新日记
        
        Args:
            title: 日记标题
            content: 日记内容
            mood: 心情（默认neutral）
        
        Returns:
            新添加日记的ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        word_count = len(content)
        
        cursor.execute('''
            INSERT INTO diaries (title, content, mood, created_date, modified_date, word_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, mood, now.date(), now, word_count))
        
        conn.commit()
        diary_id = cursor.lastrowid
        conn.close()
        
        print(f"✅ 日记已保存，ID: {diary_id}")
        return diary_id
    
    def get_all_diaries(self) -> List[Dict]:
        """
        获取所有日记（仅标题和日期）
        
        Returns:
            日记列表，每条包含 id, title, created_date, mood
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使用Row工厂，返回字典
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, created_date, mood
            FROM diaries
            ORDER BY created_date DESC, id DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # 转换为字典列表
        diaries = [dict(row) for row in rows]
        print(f"📚 查询到 {len(diaries)} 条日记")
        return diaries
    
    def get_diary(self, diary_id: int) -> Optional[Dict]:
        """
        获取指定ID的日记详情
        
        Args:
            diary_id: 日记ID
        
        Returns:
            日记详情字典，如果不存在返回None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, mood, created_date, modified_date, word_count
            FROM diaries
            WHERE id = ?
        ''', (diary_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            diary = dict(row)
            print(f"📖 读取日记: {diary['title']}")
            return diary
        else:
            print(f"❌ 未找到ID为 {diary_id} 的日记")
            return None
    
    def update_diary(self, diary_id: int, title: str, content: str, mood: str = 'neutral') -> bool:
        """
        更新日记
        
        Args:
            diary_id: 日记ID
            title: 新标题
            content: 新内容
            mood: 新心情
        
        Returns:
            是否更新成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        word_count = len(content)
        
        cursor.execute('''
            UPDATE diaries
            SET title = ?, content = ?, mood = ?, modified_date = ?, word_count = ?
            WHERE id = ?
        ''', (title, content, mood, now, word_count, diary_id))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        if affected > 0:
            print(f"✅ 日记已更新，ID: {diary_id}")
            return True
        else:
            print(f"❌ 更新失败，未找到ID为 {diary_id} 的日记")
            return False
    
    def delete_diary(self, diary_id: int) -> bool:
        """
        删除日记
        
        Args:
            diary_id: 日记ID
        
        Returns:
            是否删除成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM diaries WHERE id = ?', (diary_id,))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        if affected > 0:
            print(f"✅ 日记已删除，ID: {diary_id}")
            return True
        else:
            print(f"❌ 删除失败，未找到ID为 {diary_id} 的日记")
            return False
    
    def search_diaries(self, keyword: str) -> List[Dict]:
        """
        搜索日记（标题和内容）
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的日记列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{keyword}%"
        cursor.execute('''
            SELECT id, title, created_date, mood
            FROM diaries
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_date DESC
        ''', (search_term, search_term))
        
        rows = cursor.fetchall()
        conn.close()
        
        diaries = [dict(row) for row in rows]
        print(f"🔍 搜索 '{keyword}' 找到 {len(diaries)} 条结果")
        return diaries
    
    def get_statistics(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计数据字典
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总日记数
        cursor.execute('SELECT COUNT(*) FROM diaries')
        total_count = cursor.fetchone()[0]
        
        # 总字数
        cursor.execute('SELECT SUM(word_count) FROM diaries')
        total_words = cursor.fetchone()[0] or 0
        
        # 平均字数
        avg_words = total_words // total_count if total_count > 0 else 0
        
        conn.close()
        
        stats = {
            'total_count': total_count,
            'total_words': total_words,
            'avg_words': avg_words
        }
        
        print(f"📊 统计: {total_count} 篇日记, 共 {total_words} 字")
        return stats


# 测试代码
if __name__ == '__main__':
    print("=== 数据库模块测试 ===\n")
    
    # 创建数据库管理器
    db = DatabaseManager("test_diary.db")
    
    # 添加测试数据
    print("\n1. 添加日记")
    id1 = db.add_diary("第一天", "今天开始学习PyQt6，很兴奋！", "happy")
    id2 = db.add_diary("学习笔记", "学会了布局管理和信号槽机制。", "neutral")
    
    # 查询所有日记
    print("\n2. 查询所有日记")
    all_diaries = db.get_all_diaries()
    for diary in all_diaries:
        print(f"  - [{diary['id']}] {diary['title']} ({diary['created_date']})")
    
    # 查询单条日记
    print("\n3. 查询单条日记")
    diary = db.get_diary(id1)
    if diary:
        print(f"  标题: {diary['title']}")
        print(f"  内容: {diary['content']}")
        print(f"  字数: {diary['word_count']}")
    
    # 更新日记
    print("\n4. 更新日记")
    db.update_diary(id1, "第一天（已更新）", "今天开始学习PyQt6，很兴奋！还学会了数据库操作。", "happy")
    
    # 搜索日记
    print("\n5. 搜索日记")
    results = db.search_diaries("PyQt6")
    print(f"  找到 {len(results)} 条匹配的日记")
    
    # 统计信息
    print("\n6. 统计信息")
    stats = db.get_statistics()
    print(f"  总日记数: {stats['total_count']}")
    print(f"  总字数: {stats['total_words']}")
    print(f"  平均字数: {stats['avg_words']}")
    
    # 删除日记
    print("\n7. 删除日记")
    db.delete_diary(id2)
    
    print("\n=== 测试完成 ===")
