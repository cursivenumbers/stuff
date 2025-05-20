;; Make Emacs use UTF-8
(set-language-environment "utf-8")
(set-default-coding-systems 'utf-8-unix)
(set-keyboard-coding-system 'utf-8-unix)
(set-terminal-coding-system 'utf-8-unix)

;; Appearence settings
(load-theme 'leuven t)
(tool-bar-mode -1)
(scroll-bar-mode -1)
(setq inhibit-startup-screen t)
(global-display-line-numbers-mode)
(electric-pair-mode 1)
(global-hl-line-mode 1)
;; (set-frame-font "Consolas-26" t t )
(set-face-attribute 'default nil :font "Liberation Mono 16") 
;; Quality of Life features
(setq-default c-default-style "bsd"
	      c-basic-offset 2)
(dolist (hook '(text-mode-hook))
  (add-hook hook (lambda()
		   (flyspell-mode 1)
		   (ruler-mode 1))))
(setq-default word-wrap t)
(setq-default fill-column 72)

;; Prevent Emacs from spamming the working directory
(setq auto-save-file-name-transforms
      '((".*" "~/.emacs.d/saves/" t)))
(setq backup-directory-alist
      '((".*" "~/.emacs.d/saves/")))

;; Add Melpa
(require 'package)
(add-to-list 'package-archives
	     '("melpa-stable" . "https://stable.melpa.org/packages/") t)

;; Install Packages (Miscellaneous)
(unless (package-installed-p 'magit)
  (package-install 'magit))
(unless (package-installed-p 'org-contrib)
  (package-install 'org-contrib))

;; Install Packages (Programming and Markup languages)
(unless (package-installed-p 'json-mode)
  (package-install 'json-mode))
(unless (package-installed-p 'markdown-mode)
  (package-install 'markdown-mode))
(unless (package-installed-p 'ca65-mode)
  (package-install 'ca65-mode))
(unless (package-installed-p 'cmake-mode)
  (package-install 'cmake-mode))

;; Requiring installed packages
(require 'json-mode)
(require 'markdown-mode)
(require 'ca65-mode)
(require 'cmake-mode)
