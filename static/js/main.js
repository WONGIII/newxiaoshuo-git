// 优雅小说 - 主JavaScript文件

document.addEventListener("DOMContentLoaded", function () {
  // 初始化所有功能
  initNavigation();
  initMessages();
  initForms();
  initAnimations();
  initResponsiveFeatures();
});

// 导航功能
function initNavigation() {
  // 用户菜单交互
  const userMenus = document.querySelectorAll(".user-menu");
  userMenus.forEach((menu) => {
    menu.addEventListener("click", function (e) {
      e.stopPropagation();
      const dropdown = this.querySelector(".dropdown-menu");
      if (dropdown) {
        dropdown.classList.toggle("active");
      }
    });
  });

  // 点击其他地方关闭下拉菜单
  document.addEventListener("click", function () {
    document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
      dropdown.classList.remove("active");
    });
  });

  // 移动端菜单 - 已移除汉堡菜单，保持水平导航栏
}

// 移动端菜单 - 已移除汉堡菜单，保持水平导航栏
function initMobileMenu() {
  // 此功能已禁用，导航栏在所有设备上都保持水平布局
  return;
}

// 消息提示功能
function initMessages() {
  const messages = document.querySelectorAll(".message");

  messages.forEach((message) => {
    // 自动消失的消息
    if (
      message.classList.contains("message-success") ||
      message.classList.contains("message-info")
    ) {
      setTimeout(() => {
        fadeOut(message);
      }, 5000);
    }

    // 可关闭的消息
    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            color: inherit;
        `;

    closeBtn.addEventListener("click", function () {
      fadeOut(message);
    });

    message.style.position = "relative";
    message.appendChild(closeBtn);
  });
}

// 淡出动画
function fadeOut(element) {
  element.style.transition = "opacity 0.3s ease, transform 0.3s ease";
  element.style.opacity = "0";
  element.style.transform = "translateX(100%)";

  setTimeout(() => {
    if (element.parentNode) {
      element.parentNode.removeChild(element);
    }
  }, 300);
}

// 表单功能
function initForms() {
  // 表单验证
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!validateForm(this)) {
        e.preventDefault();
      }
    });
  });

  // 实时表单验证
  const inputs = document.querySelectorAll(
    "input[required], textarea[required]",
  );
  inputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateField(this);
    });

    input.addEventListener("input", function () {
      clearFieldError(this);
    });
  });

  // 字符计数器
  const textareas = document.querySelectorAll("textarea[maxlength]");
  textareas.forEach((textarea) => {
    const maxLength = parseInt(textarea.getAttribute("maxlength"));
    const counter = document.createElement("div");
    counter.className = "char-counter";
    counter.style.cssText = `
            font-size: 0.8rem;
            color: var(--text-light);
            text-align: right;
            margin-top: 0.25rem;
        `;

    textarea.parentNode.appendChild(counter);

    function updateCounter() {
      const currentLength = textarea.value.length;
      counter.textContent = `${currentLength}/${maxLength}`;

      if (currentLength > maxLength * 0.9) {
        counter.style.color = "var(--warning-color)";
      } else {
        counter.style.color = "var(--text-light)";
      }
    }

    textarea.addEventListener("input", updateCounter);
    updateCounter();
  });
}

// 表单验证
function validateForm(form) {
  let isValid = true;
  const requiredFields = form.querySelectorAll(
    "input[required], textarea[required]",
  );

  requiredFields.forEach((field) => {
    if (!validateField(field)) {
      isValid = false;
    }
  });

  return isValid;
}

function validateField(field) {
  const value = field.value.trim();
  let isValid = true;

  clearFieldError(field);

  if (!value) {
    showFieldError(field, "此字段为必填项");
    isValid = false;
  } else if (field.type === "email" && !isValidEmail(value)) {
    showFieldError(field, "请输入有效的邮箱地址");
    isValid = false;
  } else if (field.type === "password" && value.length < 6) {
    showFieldError(field, "密码至少需要6位字符");
    isValid = false;
  }

  return isValid;
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function showFieldError(field, message) {
  field.style.borderColor = "var(--danger-color)";

  const errorDiv = document.createElement("div");
  errorDiv.className = "field-error";
  errorDiv.style.cssText = `
        color: var(--danger-color);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    `;
  errorDiv.textContent = message;

  field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
  field.style.borderColor = "";
  const errorDiv = field.parentNode.querySelector(".field-error");
  if (errorDiv) {
    errorDiv.remove();
  }
}

// 动画效果
function initAnimations() {
  // 滚动动画
  const animatedElements = document.querySelectorAll(
    ".novel-card, .feature-card, .stat-card",
  );

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    },
  );

  animatedElements.forEach((element) => {
    observer.observe(element);
  });

  // 平滑滚动
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// 响应式功能
function initResponsiveFeatures() {
  // 图片懒加载
  if ("IntersectionObserver" in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove("lazy");
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll("img[data-src]").forEach((img) => {
      imageObserver.observe(img);
    });
  }

  // 调整文本区域高度
  const autoResizeTextareas = document.querySelectorAll(".content-editor");
  autoResizeTextareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });

    // 初始调整
    setTimeout(() => {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    }, 100);
  });
}

// 工具函数
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function throttle(func, limit) {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// 全局事件监听
window.addEventListener(
  "resize",
  debounce(function () {
    // 移动端菜单功能已禁用
  }, 250),
);

// 导出供其他脚本使用
window.NovelApp = {
  debounce,
  throttle,
  validateForm,
  fadeOut,
};
