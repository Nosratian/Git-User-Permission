# Git-User-Permission
Git user permission for user action on git branches
----------------------------------------------------
This script (including classes) processes the sending data through the push request based on the committed information to authenticate the user for change the branches.

Manage user access to branches generated at the git using hooks.
This script implements read, write, create, delete, and admin access capabilities (extendable and extensible). It also has the ability to use asterisk characters for more flexibility in naming branches for more dynamic access.

User manual:
----------------------------------------------------
Copy all the "src" folder files into the ".git folder" and under the "hooks" folder.

مجوزهای کاربر برای اعمال تغییرات در شاخه های گیت
----------------------------------------------------
این اسکریپت (شامل کلاس ها) داده های ارسال شده از طریق درخواست "push" را بر اساس اطلاعات کامیت پردازش می کند تا کاربر را برای اجازه تغییر در شاخه ها احراز هویت کند.

مدیریت دسترسی کاربران برای شاخه های تولید شده در گیت با استفاده از هوک.
این اسکریپت قابلیت های دسترسی به صورت خواندنی، نوشتنی، ایجاد، حذف و مدیر را پیاده سازی کرده است (قابل تعمیم و توسعه می باشد).
همچنین قابلیت استفاده از کاراکتر ستاره برای انعطاف بیشتر در تعیین نام شاخه ها جهت دسترسی پویاتر را دارد.

راهنمای کاربری:
----------------------------------------------------
تمام پرونده های پوشه "src" را در پوشه ".git" و در زیر پوشه "hooks" کپی کنید.
