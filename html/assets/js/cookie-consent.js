/*===================================================
	Cookie Consent Management
====================================================*/

const CookieConsent = {
    cookieName: 'bufcan-cookie-consent',
    cookieDays: 365,

    // Initialize cookie consent banner
    init: function () {
        console.log('CookieConsent initialized');
        
        // Check if user has already made a choice
        if (!this.hasUserChoice()) {
            console.log('No cookie choice found - showing banner');
            this.showBanner();
        } else {
            console.log('Cookie choice found: ' + this.getCookie(this.cookieName));
            // Load analytics if user previously accepted
            if (this.hasAccepted()) {
                this.loadAnalytics();
            }
        }

        this.bindEvents();
    },

    // Check if user has made a cookie choice
    hasUserChoice: function () {
        return this.getCookie(this.cookieName) !== null;
    },

    // Check if user has accepted cookies
    hasAccepted: function () {
        const consent = this.getCookie(this.cookieName);
        return consent === 'accepted';
    },

    // Get cookie value
    getCookie: function (name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i].trim();
            if (c.indexOf(nameEQ) === 0) {
                return c.substring(nameEQ.length, c.length);
            }
        }
        return null;
    },

    // Set cookie
    setCookie: function (name, value, days) {
        let expires = "";
        if (days) {
            const d = new Date();
            d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + d.toUTCString();
        }
        document.cookie = name + "=" + value + expires + "; path=/; SameSite=Lax";
        console.log('Cookie set: ' + name + '=' + value);
    },

    // Show banner
    showBanner: function () {
        const bannerHTML = `
            <div class="cookie-consent-banner" id="cookieConsentBanner">
                <div class="cookie-consent-content">
                    <div class="cookie-consent-text">
                        <h4>Cookie Policy</h4>
                        <p>We use cookies to enhance your experience on our website. By continuing to browse, you agree to our use of cookies. Please review our <a href="privacy-policy.html" target="_blank">Privacy Policy</a> and <a href="terms-and-conditions.html">Terms and Conditions</a> for more information.</p>
                    </div>
                    <div class="cookie-consent-actions">
                        <button class="cookie-btn cookie-decline-btn" id="cookieDecline">Decline</button>
                        <button class="cookie-btn cookie-accept-btn" id="cookieAccept">Accept</button>
                    </div>
                </div>
            </div>
        `;

        // Use vanilla JS to append to body
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = bannerHTML;
        const banner = tempDiv.firstElementChild;
        document.body.appendChild(banner);
        console.log('Banner displayed');
    },

    // Hide banner
    hideBanner: function () {
        const banner = document.getElementById('cookieConsentBanner');
        if (banner) {
            banner.style.opacity = '0';
            banner.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                banner.remove();
                console.log('Banner removed');
            }, 300);
        }
    },

    // Load analytics (Google Analytics example)
    loadAnalytics: function () {
        console.log('Analytics loading enabled');
        // Add your analytics code here
        // Example: Google Analytics
        // window.dataLayer = window.dataLayer || [];
        // function gtag(){dataLayer.push(arguments);}
        // gtag('consent', 'update', {'analytics_storage': 'granted'});
    },

    // Bind button events
    bindEvents: function () {
        const self = this;

        document.addEventListener('click', function(e) {
            if (e.target && e.target.id === 'cookieAccept') {
                console.log('Accept button clicked');
                self.setCookie(self.cookieName, 'accepted', self.cookieDays);
                self.loadAnalytics();
                self.hideBanner();
            }

            if (e.target && e.target.id === 'cookieDecline') {
                console.log('Decline button clicked');
                self.setCookie(self.cookieName, 'declined', self.cookieDays);
                self.hideBanner();
            }
        });
    }
};

// Initialize immediately when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
        setTimeout(() => CookieConsent.init(), 100);
    });
} else {
    // DOM is already ready
    setTimeout(() => CookieConsent.init(), 100);
}
