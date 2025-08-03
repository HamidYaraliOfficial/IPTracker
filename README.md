# IPTracker

IPTracker is a Python application built with PyQt6 that allows users to look up IP address information, view lookup history, and export data to CSV. It features a multilingual interface (English, Persian, and Chinese), customizable themes, and system tray integration.

## Features

- **IP Lookup**: Retrieve detailed information about IP addresses including country, city, latitude, longitude, ISP, and more using the ip-api.com service.
- **History Tracking**: Store and view lookup history in a SQLite database.
- **Export to CSV**: Export lookup history to a CSV file.
- **Multilingual Support**: Interface available in English, Persian (فارسی), and Chinese (中文).
- **Customizable Themes**: Choose from Windows 11 Default, Light, Dark, Red, and Blue themes.
- **Auto-refresh**: Automatically refresh IP lookup at configurable intervals.
- **System Tray**: Minimize to system tray with quick access to show/hide and quit options.
- **Logging**: Maintains a log file (`ip_tracker.log`) for tracking application events.

## Requirements

- Python 3.8+
- PyQt6
- requests
- qdarkstyle

Install dependencies using:
```bash
pip install PyQt6 requests qdarkstyle
```

## Installation

1. Ensure Python 3.8 or higher is installed.
2. Install the required dependencies (see above).
3. Download or clone this repository.
4. Place the `IPTracker.jpg` icon file in the same directory as the script.
5. Run the application:
   ```bash
   python IPTracker.py
   ```

## Usage

1. **IP Lookup**:
   - Enter an IP address (e.g., `8.8.8.8`) in the input field.
   - Click the "Lookup" button or press Enter to retrieve information.
   - View results in the display area.

2. **History**:
   - View past lookups in the "History" tab.
   - Clear history or export it to a CSV file (`ip_history.csv`) in your home directory.

3. **Settings**:
   - Access via the "File" menu.
   - Change theme, language, or configure auto-refresh settings.

4. **System Tray**:
   - Minimize the app to the system tray.
   - Right-click the tray icon to show the app or quit.

## Database

- Lookup history is stored in a SQLite database located at `~/.ip_tracker/history.db`.
- The database is automatically created on first run.

## Logging

- Application events are logged to `ip_tracker.log` in the same directory as the script.
- Logs include lookup successes, failures, and other significant events.

## Notes

- Requires an active internet connection for IP lookups.
- Uses the free tier of `ip-api.com` for IP information.
- Ensure the `IPTracker.jpg` icon file is present for proper UI rendering.

---

# IPTracker (فارسی)

IPTracker یک برنامه پایتون است که با استفاده از PyQt6 ساخته شده و به کاربران امکان می‌دهد اطلاعات آدرس‌های آی‌پی را جستجو کنند، تاریخچه جستجوها را مشاهده کنند و داده‌ها را به فرمت CSV صادر کنند. این برنامه دارای رابط کاربری چندزبانه (انگلیسی، فارسی و چینی)، تم‌های قابل تنظیم و یکپارچگی با سینی سیستم است.

## ویژگی‌ها

- **جستجوی آی‌پی**: دریافت اطلاعات دقیق درباره آدرس‌های آی‌پی شامل کشور، شهر، عرض جغرافیایی، طول جغرافیایی، ارائه‌دهنده خدمات اینترنت و غیره با استفاده از سرویس ip-api.com.
- **پیگیری تاریخچه**: ذخیره و مشاهده تاریخچه جستجوها در پایگاه داده SQLite.
- **صادرات به CSV**: صادرات تاریخچه جستجوها به فایل CSV.
- **پشتیبانی چندزبانه**: رابط کاربری به زبان‌های انگلیسی، فارسی و چینی در دسترس است.
- **تم‌های قابل تنظیم**: انتخاب از میان تم‌های پیش‌فرض ویندوز 11، روشن، تیره، قرمز و آبی.
- **تازه‌سازی خودکار**: تازه‌سازی خودکار جستجوی آی‌پی در فواصل قابل تنظیم.
- **سینی سیستم**: مینیمایز کردن برنامه به سینی سیستم با دسترسی سریع به نمایش/مخفی کردن و خروج.
- **لاگ‌گیری**: نگهداری فایل لاگ (`ip_tracker.log`) برای پیگیری رویدادهای برنامه.

## پیش‌نیازها

- پایتون 3.8 یا بالاتر
- PyQt6
- requests
- qdarkstyle

نصب وابستگی‌ها با استفاده از:
```bash
pip install PyQt6 requests qdarkstyle
```

## نصب

1. اطمینان حاصل کنید که پایتون 3.8 یا بالاتر نصب شده است.
2. وابستگی‌های مورد نیاز را نصب کنید (به بالا مراجعه کنید).
3. این مخزن را دانلود یا کلون کنید.
4. فایل آیکون `IPTracker.jpg` را در همان پوشه اسکریپت قرار دهید.
5. برنامه را اجرا کنید:
   ```bash
   python IPTracker.py
   ```

## استفاده

1. **جستجوی آی‌پی**:
   - یک آدرس آی‌پی (مثلاً `8.8.8.8`) را در فیلد ورودی وارد کنید.
   - روی دکمه "جستجو" کلیک کنید یا کلید Enter را فشار دهید تا اطلاعات دریافت شود.
   - نتایج را در ناحیه نمایش مشاهده کنید.

2. **تاریخچه**:
   - جستجوهای گذشته را در تب "تاریخچه" مشاهده کنید.
   - تاریخچه را پاک کنید یا به فایل CSV (`ip_history.csv`) در پوشه خانگی خود صادر کنید.

3. **تنظیمات**:
   - از طریق منوی "فایل" دسترسی پیدا کنید.
   - تم، زبان یا تنظیمات تازه‌سازی خودکار را تغییر دهید.

4. **سینی سیستم**:
   - برنامه را به سینی سیستم مینیمایز کنید.
   - روی آیکون سینی راست‌کلیک کنید تا برنامه را نمایش دهید یا خارج شوید.

## پایگاه داده

- تاریخچه جستجوها در پایگاه داده SQLite در مسیر `~/.ip_tracker/history.db` ذخیره می‌شود.
- پایگاه داده در اولین اجرا به‌طور خودکار ایجاد می‌شود.

## لاگ‌گیری

- رویدادهای برنامه در فایل `ip_tracker.log` در همان پوشه اسکریپت ذخیره می‌شوند.
- لاگ‌ها شامل موفقیت‌ها، شکست‌ها و سایر رویدادهای مهم هستند.

## نکات

- برای جستجوی آی‌پی نیاز به اتصال فعال به اینترنت است.
- از نسخه رایگان `ip-api.com` برای اطلاعات آی‌پی استفاده می‌شود.
- اطمینان حاصل کنید که فایل آیکون `IPTracker.jpg` برای رندر صحیح رابط کاربری موجود باشد.

---

# IPTracker (中文)

IPTracker 是一个使用 PyQt6 构建的 Python 应用程序，允许用户查询 IP 地址信息、查看查询历史记录并将数据导出为 CSV 格式。它具有多语言界面（英语、波斯语和中文）、可自定义主题和系统托盘集成。

## 功能

- **IP 查询**：使用 ip-api.com 服务获取有关 IP 地址的详细信息，包括国家、城市、纬度、经度、互联网服务提供商等。
- **历史记录跟踪**：在 SQLite 数据库中存储和查看查询历史记录。
- **导出为 CSV**：将查询历史记录导出为 CSV 文件。
- **多语言支持**：界面支持英语、波斯语（فارسی）和中文（中文）。
- **可自定义主题**：可选择 Windows 11 默认、浅色、深色、红色和蓝色主题。
- **自动刷新**：以可配置的间隔自动刷新 IP 查询。
- **系统托盘**：将应用程序最小化到系统托盘，快速访问显示/隐藏和退出选项。
- **日志记录**：维护日志文件（`ip_tracker.log`）以跟踪应用程序事件。

## 要求

- Python 3.8+
- PyQt6
- requests
- qdarkstyle

使用以下命令安装依赖项：
```bash
pip install PyQt6 requests qdarkstyle
```

## 安装

1. 确保已安装 Python 3.8 或更高版本。
2. 安装所需的依赖项（见上文）。
3. 下载或克隆此存储库。
4. 将 `IPTracker.jpg` 图标文件放置在与脚本相同的目录中。
5. 运行应用程序：
   ```bash
   python IPTracker.py
   ```

## 使用

1. **IP 查询**：
   - 在输入字段中输入 IP 地址（例如 `8.8.8.8`）。
   - 单击“查询”按钮或按 Enter 键以检索信息。
   - 在显示区域查看结果。

2. **历史记录**：
   - 在“历史记录”选项卡中查看过去的查询。
   - 清除历史记录或将其导出到您家目录中的 CSV 文件（`ip_history.csv`）。

3. **设置**：
   - 通过“文件”菜单访问。
   - 更改主题、语言或配置自动刷新设置。

4. **系统托盘**：
   - 将应用程序最小化到系统托盘。
   - 右键单击托盘图标以显示应用程序或退出。

## 数据库

- 查询历史记录存储在位于 `~/.ip_tracker/history.db` 的 SQLite 数据库中。
- 数据库在首次运行时自动创建。

## 日志记录

- 应用程序事件记录在与脚本相同目录下的 `ip_tracker.log` 文件中。
- 日志包括查询成功、失败和其他重要事件。

## 注意事项

- IP 查询需要活跃的互联网连接。
- 使用 `ip-api.com` 的免费层进行 IP 信息查询。
- 确保 `IPTracker.jpg` 图标文件存在以正确渲染用户界面。