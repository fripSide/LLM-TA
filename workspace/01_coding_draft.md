# 密码安全用户研究 - 初始编码

> 请仔细阅读下列编码，勾选您认为有意义的编码 `[x]`，修改文字，或添加新的编码。
> **注意**: 请勿修改 `<!-- ID: ... -->` 注释中的内容。

## 编码列表


- [ ] **C001**: Pattern-based password generation strategy
  - 原文: "就还是用我那个老密码呗，后面加个1或者2。如果是必须要大写字母，我就把首字母大写。"
  <!-- ID: C001 | P: P01 -->


- [ ] **C002**: Reliance on a single master password
  - 原文: "反正我记不住那么多密码，基本都是一个主密码变来变去。"
  <!-- ID: C002 | P: P01 -->


- [ ] **C003**: Perception of passwords as obsolete due to SMS login
  - 原文: "反正现在都能手机号登录，密码基本也就是个摆设。"
  <!-- ID: C003 | P: P01 -->


- [ ] **C004**: Tiered security behavior based on asset value
  - 原文: "银行卡那是6位数字密码，那个肯定不一样... 其他的网站，只要不是很重要的，我就随便设个简单的。"
  <!-- ID: C004 | P: P01 -->


- [ ] **C005**: Financial loss as the primary security concern
  - 原文: "钱吧，肯定怕钱被转走。至于聊天记录啥的，也没啥见不得人的，不怕看。"
  <!-- ID: C005 | P: P01 -->


- [ ] **C006**: Cognitive overload from complex security policies
  - 原文: "每次强制改密码，我都得想半天，改完了下次肯定忘。"
  <!-- ID: C006 | P: P01 -->


- [ ] **C007**: Unsecure storage of credentials in plain text
  - 原文: "所以我现在都把新改的密码写在手机备忘录里，不然根本记不住。"
  <!-- ID: C007 | P: P01 -->


- [ ] **C008**: Optimism bias regarding security threats
  - 原文: "听说过啊，新闻里老说。但我感觉跟我没啥关系，我也没什么钱。"
  <!-- ID: C008 | P: P01 -->


- [ ] **C009**: Apathy towards post-breach security hygiene
  - 原文: "我就申诉找回来了，也没改密码，太麻烦了。"
  <!-- ID: C009 | P: P01 -->


- [ ] **C010**: Biometrics prioritized for convenience over security
  - 原文: "人脸识别我也开，主要是不是为了安全，是为了方便，不用输密码了嘛。"
  <!-- ID: C010 | P: P01 -->


- [ ] **C011**: Account abandonment due to recovery friction
  - 原文: "最后它说我账号被锁定了，让我找客服。我一气之下就注册了个新的，不登了。"
  <!-- ID: C011 | P: P01 -->


- [ ] **C012**: Unsecure password sharing via social apps
  - 原文: "视频会员经常借给朋友。我就直接微信发过去呗。"
  <!-- ID: C012 | P: P01 -->


- [ ] **C013**: Ignoring security alerts based on functional heuristics
  - 原文: "收到过，但我看了一眼，也不知道是真是假，就没管。反正到现在号也能用，应该没事吧。"
  <!-- ID: C013 | P: P01 -->


- [ ] **C014**: Desire for zero-cognitive-load authentication
  - 原文: "最好就是不用密码，走哪里都刷脸... 别让我动脑子去记那些乱七八糟的字符。"
  <!-- ID: C014 | P: P01 -->


- [ ] **C015**: Service abandonment due to registration fatigue
  - 原文: "我觉得太麻烦了，有时候为了看个文章还得注册，我就直接关了不看了。"
  <!-- ID: C015 | P: P01 -->


- [ ] **C016**: Context-dependent password creation strategy
  - 原文: "看情况。如果是重要的，比如工作账号，我会由两个常用的单词组合加上当前的年份。如果是一次性的网站，就浏览器自动生成一个强密码"
  <!-- ID: C016 | P: P02 -->


- [ ] **C017**: Reliance on browser-based password managers
  - 原文: "先看 Chrome 浏览器有没有记住。如果记住了就直接填充。"
  <!-- ID: C017 | P: P02 -->


- [ ] **C018**: Tiered password security classification
  - 原文: "设计了分级的。T1 是银行、主邮箱、微信，用最复杂的且不重复的。T2 是京东、美团这种，用另一套。T3 就是各种论坛"
  <!-- ID: C018 | P: P02 -->


- [ ] **C019**: Intentional password reuse for low-risk accounts
  - 原文: "T3 就是各种论坛，基本全一样，丢了也无所谓。"
  <!-- ID: C019 | P: P02 -->


- [ ] **C020**: Perception of 'Domino Effect' risk via email compromise
  - 原文: "主邮箱被盗。因为很多其他账号都能通过邮箱找回密码。一旦邮箱丢了，就像多米诺骨牌一样全完了。"
  <!-- ID: C020 | P: P02 -->


- [ ] **C021**: Negative perception of mandatory password rotation
  - 原文: "定期更换是最愚蠢的策略。NIST 早就说不推荐定期更换了。"
  <!-- ID: C021 | P: P02 -->


- [ ] **C022**: Predictable modification behavior due to forced rotation
  - 原文: "这只会逼着用户把密码改成 Password01, Password02。我每次遇到这种强制要求都很反感，只能被迫用一些规律性的变化。"
  <!-- ID: C022 | P: P02 -->


- [ ] **C023**: Proactive use of breach monitoring tools
  - 原文: "现在看到那种大规模泄露的新闻，我会去 HaveIBeenPwned 查一下。"
  <!-- ID: C023 | P: P02 -->


- [ ] **C024**: Strong preference for 2FA/Authenticator apps
  - 原文: "只要支持 2FA 的我都开。特别是 Google Authenticator，比短信安全。"
  <!-- ID: C024 | P: P02 -->


- [ ] **C025**: Data loss due to forgotten credentials
  - 原文: "死活想不起来，密保问题的答案也忘了。最后只能放弃，里面的照片估计也没了。"
  <!-- ID: C025 | P: P02 -->


- [ ] **C026**: Physical methods for password sharing
  - 原文: "我是直接写在便签纸上贴在家里 iPad 背面。"
  <!-- ID: C026 | P: P02 -->


- [ ] **C027**: Obfuscated digital sharing practices
  - 原文: "线上发的话，发完我会撤回，或者分两段发。"
  <!-- ID: C027 | P: P02 -->


- [ ] **C028**: Desire for passwordless/biometric authentication
  - 原文: "就是像现在的 Passkey（通行密钥）那样吧。不需要密码，直接生物识别验证。"
  <!-- ID: C028 | P: P02 -->


- [ ] **C029**: Frustration with inconsistent platform restrictions
  - 原文: "很多网站的密码规则太奇葩了，有的不让用特殊符号，有的限制长度... 这我就很不理解"
  <!-- ID: C029 | P: P02 -->


- [ ] **C030**: Reliance on password manager for storage
  - 原文: "我用 1Password 管理，里面记录了大概 350 多个条目。"
  <!-- ID: C030 | P: P03 -->


- [ ] **C031**: Generation of long random passwords
  - 原文: "生成 20 位随机字符，保存，填入。"
  <!-- ID: C031 | P: P03 -->


- [ ] **C032**: Zero-knowledge strategy for specific passwords
  - 原文: "我根本不知道那个密码是啥。"
  <!-- ID: C032 | P: P03 -->


- [ ] **C033**: Abandonment of untracked accounts
  - 原文: "如果没有... 那就说明我没注册过，或者当时注册那个号太不重要我都没存。没存的话基本就放弃了"
  <!-- ID: C033 | P: P03 -->


- [ ] **C034**: Unique password for every account
  - 原文: "每一个，我是说每一个账号，密码都不一样。因为全是随机生成的。"
  <!-- ID: C034 | P: P03 -->


- [ ] **C035**: Physical backup of master password
  - 原文: "记在了一张纸条上放在保险柜里，以防我失忆。"
  <!-- ID: C035 | P: P03 -->


- [ ] **C036**: Frustration with rigid password composition rules
  - 原文: "这种规则对真正的密码管理器用户很不友好。有时候生成的随机密码不符合它的规则"
  <!-- ID: C036 | P: P03 -->


- [ ] **C037**: Skepticism towards mandatory password rotation
  - 原文: "定期更换也是，毫无意义的安全剧场。"
  <!-- ID: C037 | P: P03 -->


- [ ] **C038**: Perceived high barrier to entry for password managers
  - 原文: "但由于上手门槛太高，他们基本都不用。"
  <!-- ID: C038 | P: P03 -->


- [ ] **C039**: Preference for Hardware/App-based 2FA over SMS
  - 原文: "我不用短信验证码，不安全。我用 YubiKey 这种硬件 Key，或者 Authy 这种 APP。"
  <!-- ID: C039 | P: P03 -->


- [ ] **C040**: Secure password sharing via family vault features
  - 原文: "我用 1Password 的家庭共享功能。把需要的条目放到共享保险库里"
  <!-- ID: C040 | P: P03 -->


- [ ] **C041**: Desire for OS-level seamless integration
  - 原文: "希望操作系统层面能打通，不管是在 PC 浏览器还是手机 APP，都能一键识别并填充。"
  <!-- ID: C041 | P: P03 -->


- [ ] **C042**: Poor app compatibility with password autofill
  - 原文: "国内很多 APP 不支持标准的密码填充 API，导致还要手动切出去复制粘贴，体验极差。"
  <!-- ID: C042 | P: P03 -->



---

## 使用说明

1. 使用 `[x]` 勾选有意义的编码
2. 可以直接修改编码文本来润色或纠正
3. 可以在列表末尾添加新的编码（保持相同格式）
4. 完成后运行 `llm-ta theming` 生成主题