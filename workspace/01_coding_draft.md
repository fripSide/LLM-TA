# 密码安全用户研究 - 初始编码

> 请仔细阅读下列编码，勾选您认为有意义的编码 `[x]`，修改文字，或添加新的编码。
> **注意**: 请勿修改 `<!-- ID: ... -->` 注释中的内容。

## 编码列表


- [x] **C001**: Pattern-based password modification
  - 原文: "就还是用我那个老密码呗，后面加个1或者2。如果是必须要大写字母，我就把首字母大写。"
  <!-- ID: C001 | P: P01 -->


- [x] **C002**: Master password strategy
  - 原文: "基本都是一个主密码变来变去。"
  <!-- ID: C002 | P: P01 -->


- [x] **C003**: Reliance on SMS/OTP over static passwords
  - 原文: "反正现在都能手机号登录，密码基本也就是个摆设。"
  <!-- ID: C003 | P: P01 -->


- [x] **C004**: Password reuse across related ecosystems
  - 原文: "像支付宝登录密码，其实和我淘宝密码是一样的，因为是一家的嘛。"
  <!-- ID: C004 | P: P01 -->


- [x] **C005**: Financial loss as primary security motivator
  - 原文: "钱吧，肯定怕钱被转走。至于聊天记录啥的，也没啥见不得人的，不怕看。"
  <!-- ID: C005 | P: P01 -->


- [x] **C006**: Insecure storage in digital notes
  - 原文: "所以我现在都把新改的密码写在手机备忘录里，不然根本记不住。"
  <!-- ID: C006 | P: P01 -->


- [x] **C007**: Low perceived personal risk/value
  - 原文: "但我感觉跟我没啥关系，我也没什么钱。"
  <!-- ID: C007 | P: P01 -->


- [x] **C008**: Neglecting remediation after breach due to inconvenience
  - 原文: "我就申诉找回来了，也没改密码，太麻烦了。"
  <!-- ID: C008 | P: P01 -->


- [x] **C009**: Biometrics prioritized for convenience rather than security
  - 原文: "人脸识别我也开，主要是不是为了安全，是为了方便，不用输密码了嘛。"
  <!-- ID: C009 | P: P01 -->


- [x] **C010**: Account abandonment due to recovery friction
  - 原文: "最后它说我账号被锁定了，让我找客服。我一气之下就注册了个新的，不登了。"
  <!-- ID: C010 | P: P01 -->


- [x] **C011**: Unencrypted password sharing via messaging apps
  - 原文: "视频会员经常借给朋友。我就直接微信发过去呗。"
  <!-- ID: C011 | P: P01 -->


- [x] **C012**: Ignoring security alerts
  - 原文: "收到过，但我看了一眼，也不知道是真是假，就没管。"
  <!-- ID: C012 | P: P01 -->


- [x] **C013**: Desire for passwordless experience
  - 原文: "最好就是不用密码，走哪里都刷脸。"
  <!-- ID: C013 | P: P01 -->


- [x] **C014**: Security fatigue causing user churn
  - 原文: "我觉得太麻烦了，有时候为了看个文章还得注册，我就直接关了不看了。"
  <!-- ID: C014 | P: P01 -->


- [x] **C015**: Context-dependent password creation strategy
  - 原文: "看情况。如果是重要的，比如工作账号... 如果是一次性的网站，就浏览器自动生成一个强密码"
  <!-- ID: C015 | P: P02 -->


- [x] **C016**: Pattern-based password construction for memory
  - 原文: "我会由两个常用的单词组合加上当前的年份。"
  <!-- ID: C016 | P: P02 -->


- [x] **C017**: Reliance on browser autofill for retrieval
  - 原文: "先看 Chrome 浏览器有没有记住。如果记住了就直接填充。"
  <!-- ID: C017 | P: P02 -->


- [x] **C018**: Tiered account security classification
  - 原文: "设计了分级的。T1 是银行、主邮箱、微信... T2 是京东、美团... T3 就是各种论坛"
  <!-- ID: C018 | P: P02 -->


- [x] **C019**: Intentional password reuse for low-risk accounts
  - 原文: "T3 就是各种论坛，基本全一样，丢了也无所谓。"
  <!-- ID: C019 | P: P02 -->


- [x] **C020**: Perception of email as a single point of failure
  - 原文: "主邮箱被盗。因为很多其他账号都能通过邮箱找回密码。一旦邮箱丢了，就像多米诺骨牌一样全完了。"
  <!-- ID: C020 | P: P02 -->


- [x] **C021**: Negative attitude toward mandatory password rotation
  - 原文: "定期更换是最愚蠢的策略... 我每次遇到这种强制要求都很反感"
  <!-- ID: C021 | P: P02 -->


- [x] **C022**: Predictable modification patterns due to forced rotation
  - 原文: "这只会逼着用户把密码改成 Password01, Password02... 只能被迫用一些规律性的变化。"
  <!-- ID: C022 | P: P02 -->


- [x] **C023**: Reactive security behavior following a breach
  - 原文: "CSDN 泄露那次我就中招了。之后我就把所有重要账号密码全改了一遍。"
  <!-- ID: C023 | P: P02 -->


- [x] **C024**: Use of third-party tools to check for breaches
  - 原文: "现在看到那种大规模泄露的新闻，我会去 HaveIBeenPwned 查一下。"
  <!-- ID: C024 | P: P02 -->


- [x] **C025**: Proactive adoption of Two-Factor Authentication (2FA)
  - 原文: "只要支持 2FA 的我都开。特别是 Google Authenticator... 虽然稍微麻烦点，但心里踏实。"
  <!-- ID: C025 | P: P02 -->


- [x] **C026**: Data loss due to forgotten credentials
  - 原文: "死活想不起来，密保问题的答案也忘了。最后只能放弃，里面的照片估计也没了。"
  <!-- ID: C026 | P: P02 -->


- [x] **C027**: Physical recording for shared household passwords
  - 原文: "比如 Netflix 账号给家里人用。我是直接写在便签纸上贴在家里 iPad 背面。"
  <!-- ID: C027 | P: P02 -->


- [x] **C028**: Obfuscation strategies when sharing passwords digitally
  - 原文: "线上发的话，发完我会撤回，或者分两段发。"
  <!-- ID: C028 | P: P02 -->


- [x] **C029**: Preference for passwordless/biometric authentication
  - 原文: "就是像现在的 Passkey（通行密钥）那样吧。不需要密码，直接生物识别验证。"
  <!-- ID: C029 | P: P02 -->


- [x] **C030**: Frustration with inconsistent password composition rules
  - 原文: "很多网站的密码规则太奇葩了... 限制长度不能超过16位... 限制长度是帮黑客爆破吗？"
  <!-- ID: C030 | P: P02 -->


- [x] **C031**: Reliance on password manager for storage
  - 原文: "我用 1Password 管理，里面记录了大概 350 多个条目。"
  <!-- ID: C031 | P: P03 -->


- [x] **C032**: Generation of long random characters
  - 原文: "生成 20 位随机字符，保存，填入。我根本不知道那个密码是啥。"
  <!-- ID: C032 | P: P03 -->


- [x] **C033**: Abandonment of unmanaged accounts
  - 原文: "如果没有... 那就说明我没注册过，或者当时注册那个号太不重要我都没存。没存的话基本就放弃了"
  <!-- ID: C033 | P: P03 -->


- [x] **C034**: Unique passwords for every account
  - 原文: "每一个，我是说每一个账号，密码都不一样。因为全是随机生成的。"
  <!-- ID: C034 | P: P03 -->


- [x] **C035**: Physical backup for master password
  - 原文: "所以我把主密码设得巨长，而且记在了一张纸条上放在保险柜里，以防我失忆。"
  <!-- ID: C035 | P: P03 -->


- [x] **C036**: Frustration with rigid composition rules
  - 原文: "这种规则对真正的密码管理器用户很不友好。有时候生成的随机密码不符合它的规则（比如必须有大写），我还得手动调整。"
  <!-- ID: C036 | P: P03 -->


- [x] **C037**: Skepticism towards mandatory password rotation
  - 原文: "定期更换也是，毫无意义的安全剧场。"
  <!-- ID: C037 | P: P03 -->


- [x] **C038**: High learning curve barrier for others
  - 原文: "每次听说我都会给朋友安利密码管理器，但由于上手门槛太高，他们基本都不用。"
  <!-- ID: C038 | P: P03 -->


- [x] **C039**: Preference for hardware/app-based 2FA
  - 原文: "我不用短信验证码，不安全。我用 YubiKey 这种硬件 Key，或者 Authy 这种 APP。"
  <!-- ID: C039 | P: P03 -->


- [x] **C040**: Secure sharing via tool features
  - 原文: "我用 1Password 的家庭共享功能... 绝对不通过微信发明文密码。"
  <!-- ID: C040 | P: P03 -->


- [x] **C041**: Usability friction in local apps
  - 原文: "国内很多 APP 不支持标准的密码填充 API，导致还要手动切出去复制粘贴，体验极差。"
  <!-- ID: C041 | P: P03 -->


- [x] **C042**: Desire for OS-level integration
  - 原文: "希望操作系统层面能打通，不管是在 PC 浏览器还是手机 APP，都能一键识别并填充。"
  <!-- ID: C042 | P: P03 -->



---

## 使用说明

1. 使用 `[x]` 勾选有意义的编码
2. 可以直接修改编码文本来润色或纠正
3. 可以在列表末尾添加新的编码（保持相同格式）
4. 完成后运行 `llm-ta theming` 生成主题