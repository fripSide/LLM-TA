# 密码安全用户研究 - 主题分析

> 以下是基于已选编码生成的初步主题。
> 您可以：移动编码到其他主题、修改主题名称、合并或拆分主题。
> **注意**: 请勿修改 `<!-- THEME_ID: ... -->` 和 `<!-- CODE_ID: ... -->` 注释。


### The Spectrum of Management Strategies: From Cognitive Patterns to Technological Offloading
<!-- THEME_ID: T01 -->
Participants demonstrated a distinct dichotomy in their approach to password construction and storage, ranging from reliance on human memory to the adoption of specialized software. A significant portion of users employed cognitive strategies to maintain access, such as utilizing a single 'master password' across multiple sites, constructing passwords based on memorable patterns (e.g., combining words with years), or modifying a base password with predictable suffixes. For these users, the primary goal was memorability, often leading to insecure storage habits like writing credentials in digital notes or relying on browser autofill features.

Conversely, a subset of participants adopted a technology-centric approach, offloading the cognitive burden to password managers. These users prioritized entropy over memorability, generating long, random character strings unique to every account. While this strategy significantly enhanced security by eliminating reuse, it introduced new dependencies, such as the critical need to secure the master password—sometimes via physical backups—and reliance on the software's availability. This theme highlights the fundamental trade-off users navigate between the convenience of memory-based access and the security of tool-assisted management.


- **C001**: Pattern-based password modification
  - _"就还是用我那个老密码呗，后面加个1或者2。如果是必须要大写字母，我就把首字母大写。"_ (P01)
  <!-- CODE_ID: C001 -->

- **C002**: Master password strategy
  - _"基本都是一个主密码变来变去。"_ (P01)
  <!-- CODE_ID: C002 -->

- **C004**: Password reuse across related ecosystems
  - _"像支付宝登录密码，其实和我淘宝密码是一样的，因为是一家的嘛。"_ (P01)
  <!-- CODE_ID: C004 -->

- **C006**: Insecure storage in digital notes
  - _"所以我现在都把新改的密码写在手机备忘录里，不然根本记不住。"_ (P01)
  <!-- CODE_ID: C006 -->

- **C015**: Context-dependent password creation strategy
  - _"看情况。如果是重要的，比如工作账号... 如果是一次性的网站，就浏览器自动生成一个强密码"_ (P02)
  <!-- CODE_ID: C015 -->

- **C016**: Pattern-based password construction for memory
  - _"我会由两个常用的单词组合加上当前的年份。"_ (P02)
  <!-- CODE_ID: C016 -->

- **C017**: Reliance on browser autofill for retrieval
  - _"先看 Chrome 浏览器有没有记住。如果记住了就直接填充。"_ (P02)
  <!-- CODE_ID: C017 -->

- **C031**: Reliance on password manager for storage
  - _"我用 1Password 管理，里面记录了大概 350 多个条目。"_ (P03)
  <!-- CODE_ID: C031 -->

- **C032**: Generation of long random characters
  - _"生成 20 位随机字符，保存，填入。我根本不知道那个密码是啥。"_ (P03)
  <!-- CODE_ID: C032 -->

- **C034**: Unique passwords for every account
  - _"每一个，我是说每一个账号，密码都不一样。因为全是随机生成的。"_ (P03)
  <!-- CODE_ID: C034 -->

- **C035**: Physical backup for master password
  - _"所以我把主密码设得巨长，而且记在了一张纸条上放在保险柜里，以防我失忆。"_ (P03)
  <!-- CODE_ID: C035 -->



### Risk Perception and Tiered Security Models
<!-- THEME_ID: T02 -->
User investment in password security was rarely uniform; instead, it was heavily influenced by a personal risk assessment that prioritized financial assets over data privacy. Participants frequently described a mental tiering system where banking and primary communication accounts (Tier 1) warranted strong, unique protection, while low-risk accounts like forums (Tier 3) were subject to intentional password reuse. In this mental model, the perceived value of the account dictated the security effort, with financial loss serving as the primary motivator for vigilance.

However, this theme also revealed gaps in user risk perception. Some participants expressed a sense of invulnerability due to a lack of wealth, believing they were not targets for attackers. Others recognized the structural risks of the digital ecosystem, identifying email accounts as single points of failure that could trigger a domino effect of compromised identities. This suggests that while users apply a logical framework to security, their assessment of 'value' does not always align with the actual potential for data exploitation.


- **C005**: Financial loss as primary security motivator
  - _"钱吧，肯定怕钱被转走。至于聊天记录啥的，也没啥见不得人的，不怕看。"_ (P01)
  <!-- CODE_ID: C005 -->

- **C007**: Low perceived personal risk/value
  - _"但我感觉跟我没啥关系，我也没什么钱。"_ (P01)
  <!-- CODE_ID: C007 -->

- **C018**: Tiered account security classification
  - _"设计了分级的。T1 是银行、主邮箱、微信... T2 是京东、美团... T3 就是各种论坛"_ (P02)
  <!-- CODE_ID: C018 -->

- **C019**: Intentional password reuse for low-risk accounts
  - _"T3 就是各种论坛，基本全一样，丢了也无所谓。"_ (P02)
  <!-- CODE_ID: C019 -->

- **C020**: Perception of email as a single point of failure
  - _"主邮箱被盗。因为很多其他账号都能通过邮箱找回密码。一旦邮箱丢了，就像多米诺骨牌一样全完了。"_ (P02)
  <!-- CODE_ID: C020 -->



### Friction, Fatigue, and the Desire for Seamless Authentication
<!-- THEME_ID: T03 -->
A pervasive theme across the dataset was 'security fatigue,' where rigid security protocols conflicted with user experience, often leading to unsafe behaviors or service abandonment. Participants expressed strong frustration with mandatory password rotation and inconsistent composition rules (e.g., length limits), describing these requirements as 'security theater' that forced them into predictable behaviors like incrementing numbers. This friction caused some users to abandon account creation entirely or give up on accounts when recovery processes proved too cumbersome.

Consequently, there was a strong preference for authentication methods that minimized cognitive load. Users overwhelmingly favored biometrics and SMS/OTP logins, not necessarily for their security benefits, but for their convenience and the elimination of memory requirements. This desire for a 'passwordless' experience extended to hopes for better operating system integration and the adoption of Passkeys, highlighting a user demand for security that is invisible and frictionless rather than intrusive.


- **C003**: Reliance on SMS/OTP over static passwords
  - _"反正现在都能手机号登录，密码基本也就是个摆设。"_ (P01)
  <!-- CODE_ID: C003 -->

- **C009**: Biometrics prioritized for convenience rather than security
  - _"人脸识别我也开，主要是不是为了安全，是为了方便，不用输密码了嘛。"_ (P01)
  <!-- CODE_ID: C009 -->

- **C010**: Account abandonment due to recovery friction
  - _"最后它说我账号被锁定了，让我找客服。我一气之下就注册了个新的，不登了。"_ (P01)
  <!-- CODE_ID: C010 -->

- **C013**: Desire for passwordless experience
  - _"最好就是不用密码，走哪里都刷脸。"_ (P01)
  <!-- CODE_ID: C013 -->

- **C014**: Security fatigue causing user churn
  - _"我觉得太麻烦了，有时候为了看个文章还得注册，我就直接关了不看了。"_ (P01)
  <!-- CODE_ID: C014 -->

- **C021**: Negative attitude toward mandatory password rotation
  - _"定期更换是最愚蠢的策略... 我每次遇到这种强制要求都很反感"_ (P02)
  <!-- CODE_ID: C021 -->

- **C022**: Predictable modification patterns due to forced rotation
  - _"这只会逼着用户把密码改成 Password01, Password02... 只能被迫用一些规律性的变化。"_ (P02)
  <!-- CODE_ID: C022 -->

- **C029**: Preference for passwordless/biometric authentication
  - _"就是像现在的 Passkey（通行密钥）那样吧。不需要密码，直接生物识别验证。"_ (P02)
  <!-- CODE_ID: C029 -->

- **C030**: Frustration with inconsistent password composition rules
  - _"很多网站的密码规则太奇葩了... 限制长度不能超过16位... 限制长度是帮黑客爆破吗？"_ (P02)
  <!-- CODE_ID: C030 -->

- **C033**: Abandonment of unmanaged accounts
  - _"如果没有... 那就说明我没注册过，或者当时注册那个号太不重要我都没存。没存的话基本就放弃了"_ (P03)
  <!-- CODE_ID: C033 -->

- **C036**: Frustration with rigid composition rules
  - _"这种规则对真正的密码管理器用户很不友好。有时候生成的随机密码不符合它的规则（比如必须有大写），我还得手动调整。"_ (P03)
  <!-- CODE_ID: C036 -->

- **C037**: Skepticism towards mandatory password rotation
  - _"定期更换也是，毫无意义的安全剧场。"_ (P03)
  <!-- CODE_ID: C037 -->

- **C038**: High learning curve barrier for others
  - _"每次听说我都会给朋友安利密码管理器，但由于上手门槛太高，他们基本都不用。"_ (P03)
  <!-- CODE_ID: C038 -->

- **C041**: Usability friction in local apps
  - _"国内很多 APP 不支持标准的密码填充 API，导致还要手动切出去复制粘贴，体验极差。"_ (P03)
  <!-- CODE_ID: C041 -->

- **C042**: Desire for OS-level integration
  - _"希望操作系统层面能打通，不管是在 PC 浏览器还是手机 APP，都能一键识别并填充。"_ (P03)
  <!-- CODE_ID: C042 -->



### Interpersonal Sharing and Reactive vs. Proactive Security Behaviors
<!-- THEME_ID: T04 -->
This theme captures how users navigate the social aspects of credential sharing and their behavioral responses to security threats. Sharing passwords remained a common necessity, particularly for streaming services, but methods varied significantly in sophistication. While some users transmitted unencrypted passwords via messaging apps, others employed obfuscation techniques (e.g., retracting messages) or physical notes, and advanced users utilized secure sharing features within password managers.

Regarding threat response, the data revealed a spectrum from apathy to proactive defense. Some users ignored security alerts or neglected to change passwords after breaches due to the inconvenience, while others adopted a 'reactive' stance, mass-updating credentials only after a confirmed incident. Conversely, a segment of 'proactive' users utilized tools like 'HaveIBeenPwned' and adopted Two-Factor Authentication (2FA)—ranging from hardware keys to authenticator apps—to preemptively secure their digital lives, despite the added friction.


- **C008**: Neglecting remediation after breach due to inconvenience
  - _"我就申诉找回来了，也没改密码，太麻烦了。"_ (P01)
  <!-- CODE_ID: C008 -->

- **C011**: Unencrypted password sharing via messaging apps
  - _"视频会员经常借给朋友。我就直接微信发过去呗。"_ (P01)
  <!-- CODE_ID: C011 -->

- **C012**: Ignoring security alerts
  - _"收到过，但我看了一眼，也不知道是真是假，就没管。"_ (P01)
  <!-- CODE_ID: C012 -->

- **C023**: Reactive security behavior following a breach
  - _"CSDN 泄露那次我就中招了。之后我就把所有重要账号密码全改了一遍。"_ (P02)
  <!-- CODE_ID: C023 -->

- **C024**: Use of third-party tools to check for breaches
  - _"现在看到那种大规模泄露的新闻，我会去 HaveIBeenPwned 查一下。"_ (P02)
  <!-- CODE_ID: C024 -->

- **C025**: Proactive adoption of Two-Factor Authentication (2FA)
  - _"只要支持 2FA 的我都开。特别是 Google Authenticator... 虽然稍微麻烦点，但心里踏实。"_ (P02)
  <!-- CODE_ID: C025 -->

- **C026**: Data loss due to forgotten credentials
  - _"死活想不起来，密保问题的答案也忘了。最后只能放弃，里面的照片估计也没了。"_ (P02)
  <!-- CODE_ID: C026 -->

- **C027**: Physical recording for shared household passwords
  - _"比如 Netflix 账号给家里人用。我是直接写在便签纸上贴在家里 iPad 背面。"_ (P02)
  <!-- CODE_ID: C027 -->

- **C028**: Obfuscation strategies when sharing passwords digitally
  - _"线上发的话，发完我会撤回，或者分两段发。"_ (P02)
  <!-- CODE_ID: C028 -->

- **C039**: Preference for hardware/app-based 2FA
  - _"我不用短信验证码，不安全。我用 YubiKey 这种硬件 Key，或者 Authy 这种 APP。"_ (P03)
  <!-- CODE_ID: C039 -->

- **C040**: Secure sharing via tool features
  - _"我用 1Password 的家庭共享功能... 绝对不通过微信发明文密码。"_ (P03)
  <!-- CODE_ID: C040 -->




---

## 使用说明

1. 修改 `###` 后的文字来调整主题名称
2. 将编码条目剪切/粘贴到其他主题下进行重新分类
3. 添加新的 `### 主题名` 来创建新主题
4. 完成后运行 `llm-ta report` 生成最终报告