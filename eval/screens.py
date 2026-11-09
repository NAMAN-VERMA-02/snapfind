"""The 100 labelled eval screenshots. Each has a "twin": the same kind of screen with a few
fields changed (another month, another amount, a bus instead of a train). Twins are the hard
negatives. All brands, people, numbers and IDs are made up.

hard: jpeg = heavy JPEG artifacts, blur = downscaled to 40% and back, lowc = low-contrast text,
small = 10.5px font, tall = long scroll capture with the key content deep down.
"""

S = []


def add(id, t, twin, **fields):
    S.append({"id": id, "t": t, "twin": twin, **fields})


# ---------------------------------------------------------------- chats (phone)
add("c01", "chat", {"msgs": [("them", "Lunch on Saturday? The momo place near Sector 18", "1:02 PM"),
                             ("me", "Saturday works, 1:30?", "1:05 PM")]},
    name="Riya Sharma", msgs=[("them", "Are you free for dinner on Friday?", "6:41 PM"),
                              ("me", "Yes! Where?", "6:43 PM"),
                              ("them", "Olive Tree Cafe, 8 pm. I'll book a table for 4", "6:44 PM"),
                              ("me", "Done, see you there", "6:45 PM")])
add("c02", "chat", {"name": "Hostel Wing A", "msgs": [
    ("them", "Mess menu this week: rajma chawal Monday, paneer Wednesday", "8:10 AM"),
    ("them", "Sunday special is chole bhature", "8:11 AM")]},
    name="Hostel Wing B", sub="38 members", dark=True,
    msgs=[("them", "New wifi password for the 5G router", "10:12 PM"),
          ("them", "Network: WingB-5G   Password: maple#tiger42", "10:12 PM"),
          ("me", "Thanks bhaiya, works now", "10:20 PM")])
add("c03", "chat", {"name": "Mummy", "msgs": [("them", "Bring curd and bread on the way home", "5:30 PM"),
                                            ("me", "Ok", "5:31 PM")]},
    name="Papa", msgs=[("them", "Sent Rs 5,000 for your books. Check your account", "11:02 AM"),
                       ("me", "Got it, thank you Papa", "11:15 AM"),
                       ("them", "Buy the Operating Systems book first", "11:16 AM")])
add("c04", "chat", {"msgs": [("them", "CN lab viva is on Monday, room 110", "4:00 PM"),
                             ("me", "Which experiments?", "4:02 PM")]},
    name="Aman (CN lab)", msgs=[("them", "Lab record submission moved to Thursday 3 pm", "9:15 PM"),
                                ("them", "Room 204, bring the printed index page", "9:15 PM"),
                                ("me", "Thanks for telling", "9:20 PM")])
add("c05", "chat", {"msgs": [("them", "Plumber is coming on Sunday at 11 to fix the bathroom tap", "7:00 PM"),
                             ("me", "Ok uncle, I'll be home", "7:05 PM")]},
    name="Mr. Gupta (Landlord)", dark=True,
    msgs=[("them", "Rent of Rs 9,500 is due by the 5th of every month", "10:00 AM"),
          ("them", "Electricity bill will be separate as per the meter", "10:01 AM"),
          ("me", "Noted uncle", "10:30 AM")])
add("c06", "chat", {"msgs": [("them", "New address: House 14, Shakti Khand 2, Indirapuram", "3:20 PM")]},
    name="Priya", msgs=[("me", "Send me your address for the parcel", "3:10 PM"),
                        ("them", "Flat 302, Green Valley Apartments, Sector 62, Noida 201309", "3:12 PM"),
                        ("them", "Landmark: opposite the metro pillar 21", "3:12 PM")])
add("c07", "chat", {"msgs": [("them", "Tomorrow's coding club meetup is cancelled, exams are close", "9:00 PM")]},
    name="Coding Club", sub="214 members", hard="jpeg",
    msgs=[("them", "Hackathon registration closes tonight at 11:59 PM!", "6:00 PM"),
          ("them", "Teams of 4. Theme: tools for students. Prize pool Rs 50,000", "6:01 PM"),
          ("me", "Registered our team: Byte Bandits", "6:30 PM")])
add("c08", "chat", {"msgs": [("them", "Got 2 tickets for the India vs Australia match on Sunday!", "8:00 PM")]},
    name="Rahul", msgs=[("them", "Changed the Streamly password, new one is sunflower2026", "11:40 PM"),
                        ("them", "Use profile 3, don't touch my watchlist", "11:41 PM"),
                        ("me", "haha ok", "11:45 PM")])
add("c09", "chat", {"name": "Goa Trip 2027", "msgs": [("them", "Goa plan: train to Madgaon, beach shack stay", "2:00 PM"),
                                                    ("them", "Carry sunscreen and flip flops", "2:01 PM")]},
    name="Manali Trip 2026", sub="6 members", hard="tall",
    msgs=[("them", "Volvo bus booked from Delhi, Rs 3,200 per head including stay", "2:00 PM"),
          ("them", "Leaving 24 Dec night, back on 29 Dec", "2:01 PM"),
          ("them", "Carry warm jackets, gloves and power banks, it's -4 at night", "2:02 PM")])
add("c10", "chat", {"name": "Smile Dental", "msgs": [("them", "Reminder: scaling and cleaning on 3 Dec, 11:00 AM", "9:00 AM")]},
    name="Dr. Mehta Clinic", msgs=[("them", "Your appointment is confirmed for 18 Nov, 6:30 PM", "1:00 PM"),
                                   ("them", "Token number 14. Please bring old prescriptions", "1:00 PM"),
                                   ("me", "Thank you", "1:10 PM")])

# ---------------------------------------------------------------- emails (desktop)
OTHERS = [("CloudNest", "Weekly usage"), ("Campus Notices", "Holiday list"), ("Streamly", "New on Streamly")]
add("e01", "email", {"subject": "Update on your application - Software Engineering Intern",
                     "from": "Quanta Labs Careers", "body": [
                         "Thank you for your interest in Quanta Labs.",
                         "After careful review we will not be moving forward with your application at this time."]},
    subject="Offer letter - Software Engineering Intern", from_="BrightLoop HR <hr@brightloop.io>",
    date="Nov 4, 2026, 5:12 PM", others=OTHERS,
    body=["Dear Naman,", "We are happy to offer you the role of Software Engineering Intern.",
          "Stipend: Rs 40,000 per month. Location: Bengaluru (hybrid). Joining date: 6 January 2027.",
          "Please sign and return the attached offer letter within 7 days."])
add("e02", "email", {"subject": "Payment received - invoice CN-20261101",
                     "body": ["We received your payment of $5.00 for CloudNest Pro.", "Thank you!"]},
    subject="Your CloudNest free trial ends in 3 days", from_="CloudNest Billing", date="Nov 7, 2026",
    others=OTHERS, body=["Your 30-day free trial of CloudNest Pro ends on November 10.",
                         "Add a payment method to keep your 3 projects and 20 GB of storage.",
                         "If you do nothing, your account moves to the free plan."])
add("e03", "email", {"subject": "Mid-semester examination schedule", "body": [
    "Data Structures on 18 Sep, Discrete Mathematics on 20 Sep.", "Reporting time 9:30 AM."]},
    subject="End semester examination schedule - Odd semester 2026", from_="Examination Cell",
    date="Nov 2, 2026", others=OTHERS,
    body=["The end semester examinations will be held as follows:",
          "Compiler Design: 2 December 2026, 10:00 AM. Operating Systems: 5 December 2026, 10:00 AM.",
          "Computer Networks: 8 December 2026, 2:00 PM.", "Admit cards will be available on the portal."])
add("e04", "email", {"subject": "New sign-in to your Streamly account",
                     "body": ["We noticed a new sign-in from Chrome on Windows in Noida, India.",
                              "If this was you, you can ignore this email."]},
    subject="Reset your Streamly password", from_="Streamly Accounts", date="Oct 30, 2026", hard="small",
    others=OTHERS, body=["We received a request to reset the password for your account.",
                         "Click the button below to choose a new password. This link expires in 30 minutes.",
                         "If you did not ask for this, you can safely ignore this email."])
add("e05", "email", {"subject": "Your SkyHop itinerary: SH 618 BLR to DEL",
                     "body": ["Flight SH 618 Bengaluru to Delhi on 3 January 2027, departs 21:15.",
                              "Booking reference QX7H2M."]},
    subject="Your SkyHop itinerary: SH 512 DEL to BLR", from_="SkyHop Airlines", date="Nov 1, 2026",
    others=OTHERS, body=["Flight SH 512 Delhi to Bengaluru on 22 December 2026, departs 06:10, arrives 08:55.",
                         "Booking reference PL4K9T. Web check-in opens 48 hours before departure.",
                         "Baggage: 15 kg check-in, 7 kg cabin."])
add("e06", "email", {"subject": "Your reserved book is ready for pickup",
                     "body": ["'Database System Concepts' is ready at the circulation desk.",
                              "Please collect it within 3 days."]},
    subject="Overdue notice: Operating System Concepts", from_="Central Library", date="Oct 28, 2026",
    others=OTHERS, body=["The following book is overdue: Operating System Concepts (10th edition).",
                         "Due date was 20 October 2026. A fine of Rs 20 per day applies.",
                         "Please return it at the earliest."])
add("e07", "email", {"subject": "Registration confirmed - CodeSprint 2026",
                     "body": ["Your team Byte Bandits is registered for CodeSprint 2026.",
                              "The event starts on 21 November at 9 AM."]},
    subject="CodeSprint 2026 results", from_="CodeSprint Team", date="Nov 23, 2026", dark=True,
    others=OTHERS, body=["Congratulations! Team Byte Bandits secured 2nd place at CodeSprint 2026.",
                         "Prize money of Rs 25,000 will be transferred within 14 working days.",
                         "Certificates will be emailed to all members."])
add("e08", "email", {"subject": "Scholarship amount credited",
                     "body": ["The merit scholarship of Rs 30,000 has been credited to your account."]},
    subject="Scholarship application status: documents pending", from_="Scholarship Office",
    date="Nov 5, 2026", others=OTHERS,
    body=["Your scholarship application is incomplete.",
          "Pending documents: income certificate, caste certificate (if applicable).",
          "Upload them on the portal before 15 November 2026."])
add("x10", "email", {"subject": "Meeting notes - backend choice",
                     "body": ["We decided to go with Firebase for auth and storage.",
                              "Riya will set up the project."]},
    subject="Meeting notes - database choice", from_="Aman Verma", date="Nov 6, 2026", others=OTHERS,
    hard="blur",
    body=["Notes from today's project meeting:", "We will use PostgreSQL instead of MongoDB because our data is relational.",
          "Naman will write the schema, Riya the API. Next meeting Friday 5 PM."])

# ---------------------------------------------------------------- tickets, payments, orders (key/value cards)
add("k01", "kv", {"rows": [("PNR", "4521889013"), ("Train", "12952 Rajdhani Express"),
                           ("From", "New Delhi (NDLS)"), ("To", "Mumbai Central (MMCT)"),
                           ("Date of Journey", "14/10/2026"), ("Class", "3A"), ("Coach / Berth", "B4 / 12"),
                           ("Fare", "Rs 2,145.00")]},
    brand="RailBook", sub="E-Ticket", phone=True, buttons=["Download PDF", "Cancel ticket"],
    rows=[("PNR", "4521876630"), ("Train", "12952 Rajdhani Express"), ("From", "New Delhi (NDLS)"),
          ("To", "Mumbai Central (MMCT)"), ("Date of Journey", "14/12/2026"), ("Class", "3A"),
          ("Coach / Berth", "B2 / 34"), ("Fare", "Rs 2,145.00")])
add("k02", "kv", {"rows": [("From", "Mumbai"), ("To", "Pune"), ("Date", "05/08/2026"), ("Seat", "22"),
                           ("Fare", "Rs 700")]},
    brand="CityBus", sub="Booking confirmed", phone=True, buttons=["Track bus"],
    rows=[("From", "Pune (Swargate)"), ("To", "Mumbai (Dadar)"), ("Date", "02/08/2026"), ("Departure", "06:30"),
          ("Seat", "14"), ("Fare", "Rs 650")])
add("k03", "kv", {"rows": [("Flight", "SH 218"), ("From", "BLR"), ("To", "HYD"), ("Gate", "8"),
                           ("Seat", "21A"), ("Date", "09 Jan 2027")]},
    brand="SkyHop", sub="Boarding pass", phone=True, dark=True,
    rows=[("Flight", "SH 512"), ("From", "DEL"), ("To", "BLR"), ("Gate", "22"), ("Boarding", "05:40"),
          ("Seat", "14C"), ("Date", "22 Dec 2026")])
add("k04", "kv", {"hero": "Single journey ticket", "amount": "Rs 40", "rows": [
    ("From", "Botanical Garden"), ("To", "Rajiv Chowk"), ("Valid till", "Today 11:59 PM")]},
    brand="MetroCard", sub="Recharge", phone=True, hero="Recharge successful", amount="Rs 500",
    hero_sub="Card ending 0917", rows=[("Previous balance", "Rs 112"), ("New balance", "Rs 612"),
                                       ("Date", "08 Nov 2026, 9:02 AM")])
add("k05", "kv", {"rows": [("Ride", "Auto"), ("Pickup", "Sector 62 Metro"), ("Drop", "Northfield Institute Gate 2"),
                           ("Fare", "Rs 120"), ("Driver", "Ravi")]},
    brand="RideNow", sub="Your ride", phone=True, hard="lowc",
    rows=[("Driver", "Suresh Kumar (4.8)"), ("Car", "White hatchback KA 03 MN 4471"), ("Pickup", "Majestic Bus Stand"),
          ("Drop", "Airport Terminal 2"), ("Fare", "Rs 845"), ("Ride OTP", "4417")])
add("k06", "kv", {"rows": [("Hotel", "Pink City Inn, Jaipur"), ("Check-in", "14 Feb 2027"), ("Nights", "1"),
                           ("Amount", "Rs 2,100")]},
    brand="HotelHive", sub="Booking confirmed",
    rows=[("Hotel", "Snow Crest Cottage, Manali"), ("Check-in", "26 Dec 2026, 12 PM"), ("Nights", "2"),
          ("Guests", "6 adults, 3 rooms"), ("Amount paid", "Rs 4,800")])
add("k07", "kv", {"rows": [("Movie", "The Last Monsoon"), ("Cinema", "CineStar Logix Mall"), ("Screen", "1"),
                           ("Seats", "D 5, D 6"), ("Show", "Sun 17 Nov, 4:00 PM")]},
    brand="CineStar", sub="Tickets", hard="jpeg",
    rows=[("Movie", "Orbit Beyond (IMAX)"), ("Cinema", "CineStar Logix Mall"), ("Screen", "3"),
          ("Seats", "H 11, H 12"), ("Show", "Sat 16 Nov, 7:15 PM"), ("Booking ID", "CSX99120")])
add("k08", "kv", {"rows": [("Level", "B1"), ("Slot", "042"), ("Entry", "1:15 PM"), ("Vehicle", "UP 16 BX 1102")]},
    brand="MallPark", sub="Parking ticket", phone=True,
    rows=[("Level", "B2"), ("Slot", "117"), ("Entry", "6:42 PM"), ("Vehicle", "UP 16 CK 7781"),
          ("Rate", "Rs 40 first 2 hours")])
add("u01", "kv", {"amount": "Rs 149", "hero_sub": "To Chai Point", "rows": [("UPI ID", "chaipoint@okpay"),
                                                                            ("UPI Ref", "431298760077")]},
    brand="PayQuick", phone=True, hero="Payment successful", amount="Rs 1,499",
    hero_sub="To Riya Sharma", rows=[("UPI ID", "riya.s@okpay"), ("Date", "12 Nov 2026, 8:14 PM"),
                                     ("UPI Ref", "431298765012"), ("From", "State Bank XX4521")],
    buttons=["Share receipt", "Pay again"])
add("u02", "kv", {"amount": "Rs 950", "hero_sub": "To Ramesh Gupta", "rows": [("Note", "Electricity Oct")]},
    brand="PayQuick", phone=True, hero="Payment successful", amount="Rs 9,500",
    hero_sub="To Ramesh Gupta", rows=[("Note", "Rent November"), ("Date", "03 Nov 2026, 10:41 AM"),
                                      ("UPI Ref", "430711002345")])
add("u03", "kv", {"hero": "Payment successful", "rows": [("Biller", "City Electricity Board"),
                                                        ("Consumer no.", "220145789")]},
    brand="PayQuick", phone=True, dark=True, hero="Payment failed", amount="Rs 2,000",
    hero_sub="Money will be refunded in 3-5 working days",
    rows=[("Biller", "City Electricity Board"), ("Consumer no.", "220145789"), ("Reason", "Bank server timeout")])
add("u04", "kv", {"hero": "Received", "amount": "Rs 500", "hero_sub": "From Aman Verma", "rows": [
    ("Note", "pizza share")]},
    brand="PayQuick", phone=True, hero="Received", amount="Rs 5,000", hero_sub="From Papa",
    rows=[("Note", "books"), ("Date", "10 Nov 2026, 11:01 AM"), ("To", "State Bank XX4521")])
add("u05", "kv", {"amount": "Rs 719", "rows": [("Plan", "84 days, 2 GB/day"), ("Number", "98100 XXX12")]},
    brand="Airwave", sub="Recharge", phone=True, hero="Recharge successful", amount="Rs 299",
    rows=[("Plan", "28 days, 2 GB/day, unlimited calls"), ("Number", "98100 XXX12"),
          ("Valid till", "05 Dec 2026")])
add("u06", "kv", {"amount": "Rs 38,000", "rows": [("Purpose", "Hostel fee, odd semester"), ("Receipt no.", "HF-55120")]},
    brand="Northfield Institute of Technology", sub="Fee receipt", hero="Paid", amount="Rs 62,500",
    rows=[("Purpose", "Tuition fee, semester 5"), ("Student", "Naman Verma, CSE"), ("Receipt no.", "TF-90871"),
          ("Date", "01 Aug 2026")])
add("u07", "kv", {"hero": "All settled up", "amount": "Rs 0", "rows": [("Group", "Goa trip")]},
    brand="SplitEasy", sub="Manali trip", phone=True, hero="You owe", amount="Rs 800",
    hero_sub="to Aman", rows=[("Total spent", "Rs 19,200"), ("Your share", "Rs 3,200"),
                              ("Paid by you", "Rs 2,400")])
add("o01", "kv", {"hero": "Out for delivery", "rows": [("Item", "Transparent phone case"),
                                                      ("Order", "#SK88790")]},
    brand="ShopKart", sub="Order details", phone=True, hero="Delivered", hero_sub="Tue, 10 Nov",
    rows=[("Item", "SoundMax wireless earbuds, black"), ("Order", "#SK88812"), ("Price", "Rs 1,299"),
          ("Paid via", "PayQuick UPI")], buttons=["Return", "Rate product"])
add("o02", "kv", {"rows": [("Items", "Veg biryani x1, raita"), ("Total", "Rs 249")]},
    brand="Zappy Eats", sub="Order delivered", phone=True, hard="blur",
    rows=[("Items", "Paneer butter masala x1, butter naan x2"), ("Total", "Rs 386"),
          ("Delivered by", "Rakesh"), ("Time", "9:12 PM")])
add("o03", "kv", {"rows": [("Item", "Running shoes, size 9"), ("Type", "Exchange for size 10")]},
    brand="ShopKart", sub="Return", phone=True,
    rows=[("Item", "Running shoes, size 9"), ("Pickup", "Thu 12 Nov, 10 AM - 6 PM"),
          ("Refund", "Rs 2,499 to original payment method")])
add("o04", "kv", {"rows": [("Items", "Bananas 1 dozen, curd 400 g, rice 5 kg"), ("Total", "Rs 488")]},
    brand="FreshCart", sub="Order placed", phone=True, dark=True,
    rows=[("Items", "Milk 2 L, eggs x12, brown bread"), ("Total", "Rs 312"), ("Slot", "Tomorrow 7-9 AM")])
add("o05", "kv", {"rows": [("Item", "Vertex 15 laptop, Ryzen 5, 8 GB"), ("EMI", "Rs 3,999 x 12 months")]},
    brand="ShopKart", sub="Order confirmed",
    rows=[("Item", "Vertex 14 laptop, Core i5, 16 GB RAM, 512 GB SSD"), ("EMI", "Rs 4,583 x 12 months"),
          ("Delivery by", "Sat, 14 Nov")])
add("o06", "kv", {"rows": [("Product", "Refrigerator 260 L"), ("Warranty till", "31/01/2029")]},
    brand="CoolAir Service", sub="Warranty card", hard="small",
    rows=[("Product", "Split air conditioner 1.5 ton"), ("Serial no.", "CA15T-778812"),
          ("Installed", "02/07/2026"), ("Warranty till", "30/06/2028")])
add("o07", "kv", {"rows": [("Items", "Vitamin D3 60K x4"), ("Total", "Rs 128")]},
    brand="MediQuick", sub="Order", phone=True,
    rows=[("Items", "Paracetamol 650 x15, Cetirizine 10 mg x10"), ("Total", "Rs 146"),
          ("Note", "Prescription required for one item")])

# ---------------------------------------------------------------- terminals (desktop)
add("t01", "terminal", {"lines": ["PS D:\\shop> npm run build", "", "vite v6.0.3 building for production...",
                                  "✓ 412 modules transformed.", "dist/index.html  0.46 kB",
                                  "✓ built in 3.21s"]},
    lines=["PS D:\\shop> npm run dev", "", "> shop@1.0.0 dev", "> node server.js", "",
           "node:events:497", "      throw er; // Unhandled 'error' event",
           "Error: listen EADDRINUSE: address already in use :::3000",
           "    at Server.setupListenHandle [as _listen2] (node:net:1904:16)"])
add("t02", "terminal", {"lines": ["$ git push origin main", "Enumerating objects: 9, done.",
                                  "To github.com:naman/notes.git", "   4f1c2a1..9be77d0  main -> main"]},
    title="Git Bash", lines=["$ git push origin main", "To github.com:naman/notes.git",
                             " ! [rejected]        main -> main (non-fast-forward)",
                             "error: failed to push some refs to 'github.com:naman/notes.git'",
                             "hint: Updates were rejected because the tip of your current branch is behind",
                             "hint: its remote counterpart. Integrate the remote changes (e.g.",
                             "hint: 'git pull ...') before pushing again."])
add("t03", "terminal", {"lines": ["PS D:\\ml> python train.py", "Traceback (most recent call last):",
                                  '  File "D:\\ml\\train.py", line 2, in <module>', "    import pandas as pd",
                                  "ModuleNotFoundError: No module named 'pandas'"]},
    lines=["PS D:\\vision> python detect.py", "Traceback (most recent call last):",
           '  File "D:\\vision\\detect.py", line 1, in <module>', "    import cv2",
           "ModuleNotFoundError: No module named 'cv2'"])
add("t04", "terminal", {"lines": ["PS D:\\api> pip install fastapi", "Collecting fastapi",
                                  "Successfully installed fastapi-0.115.4 starlette-0.41.2"]},
    hard="lowc", lines=["PS D:\\nlp> pip install hnswlib", "Building wheel for hnswlib (pyproject.toml) ... error",
                        "error: Microsoft Visual C++ 14.0 or greater is required. Get it with",
                        '"Microsoft C++ Build Tools"', "ERROR: Failed building wheel for hnswlib"])
add("t05", "terminal", {"lines": ["$ docker compose up", "[+] Running 2/2", " ✔ Container db   Started",
                                  " ✔ Container api  Started"]},
    title="Ubuntu", lines=["$ docker ps", "Cannot connect to the Docker daemon at unix:///var/run/docker.sock.",
                           "Is the docker daemon running?"])
add("t06", "terminal", {"lines": ["PS D:\\java> java Main",
                                  'Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException:',
                                  "Index 5 out of bounds for length 5", "    at Main.main(Main.java:9)"]},
    lines=["PS D:\\java> javac Main.java; java Main",
           'Exception in thread "main" java.lang.NullPointerException: Cannot invoke',
           '"String.length()" because "name" is null', "    at Main.main(Main.java:14)"])
add("t07", "terminal", {"lines": ["$ ssh ubuntu@13.233.10.4", "Welcome to Ubuntu 24.04 LTS",
                                  "Last login: Sat Nov  7 18:22:01 2026"]},
    title="Git Bash", lines=["$ ssh -i key.pem ubuntu@13.233.10.4", "ubuntu@13.233.10.4: Permission denied (publickey)."])
add("t08", "terminal", {"lines": ["$ gcc graph.c", "graph.c: In function 'main':",
                                  "graph.c:12:5: error: expected ';' before 'return'"]},
    title="Ubuntu", hard="jpeg", lines=["$ gcc graph.c -o graph && ./graph", "Enter number of vertices: 5",
                                        "Segmentation fault (core dumped)"])
add("x06", "terminal", {"lines": ["$ kubectl get pods", "NAME                    READY   STATUS    RESTARTS",
                                  "api-6d8f7c9b5-x2k8p     1/1     Running   0"]},
    title="Ubuntu", lines=["$ kubectl get pods", "NAME                    READY   STATUS             RESTARTS",
                           "api-6d8f7c9b5-x2k8p     0/1     CrashLoopBackOff   7 (2m ago)",
                           "db-0                    1/1     Running            0"])

# ---------------------------------------------------------------- code (desktop)
add("d01", "code", {"tabs": ["search.py"], "lines": [
    "def linear_search(arr, target):", "    for i, x in enumerate(arr):", "        if x == target:",
    "            return i", "    return -1"]},
    tabs=["search.py", "test_search.py"], project="dsa",
    lines=["def binary_search(arr, target):", "    lo, hi = 0, len(arr) - 1", "    while lo <= hi:",
           "        mid = (lo + hi) // 2", "        if arr[mid] == target:", "            return mid",
           "        if arr[mid] < target:", "            lo = mid + 1", "        else:", "            hi = mid - 1",
           "    return -1"])
add("d02", "code", {"lines": ["CREATE TABLE students (", "    id INT PRIMARY KEY,", "    name VARCHAR(80),",
                              "    branch VARCHAR(10)", ");"]},
    tabs=["report.sql"], project="dbms-lab", statusbar="Ln 7, Col 1  UTF-8  SQL",
    lines=["SELECT s.student_id, s.name, AVG(m.marks) AS avg_marks", "FROM students s",
           "JOIN marks m ON m.student_id = s.student_id", "GROUP BY s.student_id, s.name",
           "HAVING AVG(m.marks) > 75", "ORDER BY avg_marks DESC;"])
add("d03", "code", {"lines": ["const [count, setCount] = useState(0);",
                              "return <button onClick={() => setCount(count + 1)}>{count}</button>;"]},
    tabs=["Profile.jsx", "api.js"], project="portfolio", dark=True, statusbar="Ln 9, Col 4  UTF-8  JavaScript JSX",
    lines=["useEffect(() => {", "  const controller = new AbortController();",
           "  fetch(`/api/users/${id}`, { signal: controller.signal })",
           "    .then((r) => r.json())", "    .then(setUser);", "  return () => controller.abort();",
           "}, [id]);"])
add("d04", "code", {"lines": ["queue<int> q; q.push(src); vis[src] = true;", "while (!q.empty()) {",
                              "  int u = q.front(); q.pop();", "  for (int v : adj[u]) if (!vis[v]) {",
                              "    vis[v] = true; q.push(v); }", "}"]},
    tabs=["graph.cpp"], project="dsa", statusbar="Ln 30, Col 1  UTF-8  C++", hard="small",
    lines=["priority_queue<pii, vector<pii>, greater<pii>> pq;", "dist[src] = 0; pq.push({0, src});",
           "while (!pq.empty()) {", "  auto [d, u] = pq.top(); pq.pop();", "  if (d > dist[u]) continue;",
           "  for (auto [v, w] : adj[u])", "    if (dist[u] + w < dist[v]) {",
           "      dist[v] = dist[u] + w; pq.push({dist[v], v}); }", "}"])
add("d05", "code", {"tabs": ["config.yaml"], "lines": ["server:", "  port: 8080", "logging:", "  level: info"]},
    tabs=[".env"], project="expense-api", statusbar="Ln 4, Col 1  UTF-8  Properties",
    lines=["DATABASE_URL=postgres://app:devpass@localhost:5432/expenses", "JWT_SECRET=change-me-in-prod",
           "PORT=4000", "SMTP_HOST=localhost"])
add("x07", "code", {"lines": ["const phoneRe = /^[6-9]\\d{9}$/;", "phoneRe.test('9810012345'); // true"]},
    tabs=["validate.js"], project="signup-form", statusbar="Ln 3, Col 1  UTF-8  JavaScript",
    lines=["const emailRe = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;", "export function isEmail(s) {",
           "  return emailRe.test(s.trim());", "}"])

# ---------------------------------------------------------------- settings (desktop)
add("s01", "settings", {"page": "Ethernet", "rows": [("Link speed", "1000/1000 Mbps"),
                                                     ("IPv4 address", "192.168.1.23")]},
    section="Network & internet", page="Wi-Fi", rows=[("SSID", "Northfield-Campus-5G"),
                                                      ("Protocol", "Wi-Fi 6 (802.11ax)"),
                                                      ("IPv4 address", "10.21.4.117"),
                                                      ("IPv4 DNS servers", "10.21.0.1"),
                                                      ("Physical address (MAC)", "3C-21-9E-44-0A-7B")])
add("s02", "settings", {"page": "Sound", "rows": [("Output", "Speakers (Realtek Audio)"), ("Volume", "64")]},
    section="System", page="Display", hard="blur",
    rows=[("Display resolution", "1920 × 1080 (Recommended)"), ("Scale", "125%"), ("Refresh rate", "60 Hz"),
          ("Night light", "On until 7:00 AM")])
add("s03", "settings", {"page": "Storage", "rows": [("Local disk (C:)", "212 GB used of 476 GB"),
                                                    ("Temporary files", "6.20 GB")]},
    section="System", page="About", rows=[("Device name", "LAPTOP-7Q2K"),
                                          ("Processor", "12th Gen Intel Core i3-1215U 1.20 GHz"),
                                          ("Installed RAM", "8.00 GB (7.73 GB usable)"),
                                          ("Edition", "Windows 11 Home"), ("Version", "24H2")])
add("s04", "settings", {"page": "Printers & scanners", "rows": [("InkJet 2300 series", "Offline")]},
    section="Bluetooth & devices", page="Devices", dark=True,
    rows=[("Rockerz 450 headphones", "Connected, battery 80%"), ("Wireless mouse M185", "Paired"),
          ("Bluetooth", "On")])
add("s05", "settings", {"section": "Windows Update", "page": "Updates", "rows": [
    ("2026-11 Cumulative Update for Windows 11", "Pending restart")]},
    section="Privacy", page="App permissions", rows=[("Location", "Off"), ("Camera", "On for 3 apps"),
                                                     ("Microphone", "On for 5 apps"), ("Screenshots", "On")],
    sections=["System", "Network & internet", "Apps", "Accounts", "Privacy", "Windows Update"])

# ---------------------------------------------------------------- social posts (phone)
add("p01", "post", {"text": "Annual cultural fest Tarang is on 5-7 December. Star night with live band!"},
    author="Northfield Placement Cell", handle="@nit_placements", when="2h",
    text="Campus placement drive next week: 14 companies visiting, CTC up to 18 LPA. "
         "Eligibility 7.0 CGPA. Register on the portal by Friday.")
add("p02", "post", {"text": "Pro tip: git rebase -i HEAD~3 lets you squash your last three commits."},
    author="Dev Daily", handle="@devdaily", when="5h", dark=True,
    text="Pro tip: git stash -p lets you stash only some of your changes, hunk by hunk.")
add("p03", "post", {"text": "SkyHop flight SH 512 delayed by 3 hours, no update at the gate. @SkyHop please respond"},
    author="Kunal", handle="@kunal_travels", when="1d", hard="jpeg",
    text="Train 12952 delayed by 4 hours at Kanpur, no announcement at all. @RailBook please help",
    replies=[("RailBook Care", "@railbookcare", "Sorry for the delay, please DM your PNR")])
add("p04", "post", {"text": "Get a free .dev domain for one year with your student email."},
    author="CloudNest", handle="@cloudnest", when="3d",
    text="Students get $100 of free CloudNest credits. Apply with your college email address.")
add("p05", "post", {"text": "Me: I'll sleep early tonight. Also me at 3 AM: reading about black holes"},
    author="Memes for Devs", handle="@devmemes", when="8h",
    text="When the code works on the first try: suspicious. When it fails: expected.")
add("p06", "post", {"text": "Found: blue steel water bottle in the CSE lab 3. Collect from the lab assistant."},
    author="Campus Lost & Found", handle="@nit_lostfound", when="4h",
    text="Lost: black leather wallet near the library block. Has my ID card and metro card. "
         "Please call 98xxxxxx12 if found.")

# ---------------------------------------------------------------- notes
add("n01", "notes", {"title": "Hostel packing list", "items": ["Bedsheet", "Extension board", "Bucket and mug",
                                                               "Padlock"]},
    title="Grocery list", date="Sunday", phone=True,
    items=["Atta 5 kg", "Toor dal 1 kg", "Onions", "Maggi x6", "x Detergent", "Bread"])
add("n02", "notes", {"title": "Web dev roadmap", "items": ["HTML and CSS basics", "JavaScript", "React",
                                                           "Node and Express"]},
    title="DSA revision plan", date="Nov 2026",
    items=["Mon: graphs (BFS, DFS, Dijkstra)", "Tue: dynamic programming", "Wed: trees and BST",
           "Thu: sliding window + two pointers", "Fri: mock test on LeetCode"])
add("n03", "notes", {"title": "Gift ideas for Papa", "items": ["Fitness band", "Leather belt", "Biography book"]},
    title="Gift ideas for Didi's birthday", date="Nov 2026", phone=True, dark=True,
    items=["Perfume", "Small handbag", "Scented candles", "Polaroid camera"])
add("n04", "notes", {"title": "Viva questions - Computer Networks", "items": [
    "OSI vs TCP/IP model", "TCP three-way handshake", "Subnetting example"]},
    title="Viva questions - DBMS", date="Oct 2026", hard="tall",
    items=["What is normalization? 1NF, 2NF, 3NF, BCNF", "ACID properties", "Indexing and B+ trees",
           "Difference between DELETE, TRUNCATE and DROP"])
add("n05", "notes", {"title": "TV setup", "items": ["Input: HDMI 2", "Picture mode: Movie"]},
    title="Router setup", date="Sep 2026",
    items=["SSID: HomeNet_5G", "Admin page: 192.168.0.1", "Channel 36, 80 MHz", "Firmware updated 12 Sep"])
add("n06", "notes", {"title": "Books to read", "items": ["The Psychology of Money", "Clean Code", "Sapiens"]},
    title="Movies to watch", date="Nov 2026", phone=True,
    items=["Interstellar", "Spirited Away", "3 Idiots", "x Dangal", "The Prestige"])

# ---------------------------------------------------------------- calendar (desktop)
add("a01", "calendar", {"month": "November 2026", "event": {
    "title": "Project review with Prof. Iyer", "when": "Wednesday, 4 November 2026, 11:00 - 11:30",
    "rows": [("Location", "Room LT-3")]}},
    month="December 2026", event={"title": "Project review with Prof. Iyer",
                                  "when": "Wednesday, 2 December 2026, 11:00 - 11:30",
                                  "rows": [("Location", "Room LT-3"), ("Bring", "Report draft + demo")]})
add("a02", "calendar", {"event": {"title": "Eye checkup", "when": "Saturday, 28 November 2026, 5:00 PM",
                                  "rows": [("Location", "ClearView Eye Care")]}},
    month="November 2026", event={"title": "Dentist appointment", "when": "Saturday, 21 November 2026, 10:00 AM",
                                  "rows": [("Location", "Smile Dental Clinic, Sector 18")]})
add("a03", "calendar", {"event": {"title": "Mock interview - DSA round", "when": "Friday, 13 November 2026, 6:00 PM",
                                  "rows": [("Link", "meet.example/abc-defg-hij")]}},
    month="November 2026", event={"title": "Mock interview - system design",
                                  "when": "Friday, 13 November 2026, 6:00 PM",
                                  "rows": [("Link", "meet.example/xyz-uvwt-rst"), ("With", "Senior: Karan")]})
add("a04", "calendar", {"event": {"title": "Parents' anniversary", "when": "Thursday, 7 January 2027",
                                  "rows": [("Note", "Order cake")]}, "month": "January 2027"},
    month="December 2026", hard="lowc",
    event={"title": "Amma's birthday dinner", "when": "Tuesday, 29 December 2026, 8:00 PM",
           "rows": [("Location", "Spice Route restaurant"), ("Note", "Book table for 8")]})
add("a05", "calendar", {"event": {"title": "Sprint retrospective", "when": "Friday, 20 November 2026, 4:00 PM",
                                  "rows": [("Attendees", "Naman, Riya, Aman")]}},
    month="November 2026", event={"title": "Sprint planning", "when": "Monday, 9 November 2026, 10:00 AM",
                                  "rows": [("Attendees", "Naman, Riya, Aman"), ("Agenda", "Pick stories for sprint 4")]})

# ---------------------------------------------------------------- SMS (phone)
add("m01", "sms", {"sender": "AX-SHPKRT", "msgs": [("771204 is your ShopKart verification code.", "6:10 PM")]},
    sender="VM-PAYQCK", msgs=[("482913 is your OTP for PayQuick login. Do not share it with anyone. "
                               "Valid for 10 minutes.", "7:42 PM")])
add("m02", "sms", {"msgs": [("Rs 5,000.00 credited to A/c XX4521 on 10-11-26 by UPI. Avl bal Rs 23,320.55", "11:01 AM")]},
    sender="JD-SBIBNK", msgs=[("Rs 2,145.00 debited from A/c XX4521 on 12-11-26 to RailBook. "
                               "Avl bal Rs 18,320.55. Not you? Call 1800-000-111", "8:15 PM")])
add("m03", "sms", {"sender": "TX-TAXDPT", "msgs": [("Your tax ID update request is under process.", "3:00 PM")]},
    sender="AD-CTZNID", hard="small",
    msgs=[("Your CitizenID address update request URN 2026-11-0045 has been accepted. "
           "It will be processed in 30 days.", "12:30 PM")])
add("m04", "sms", {"msgs": [("Water bill for Nov: Rs 210 due on 25-11-2026.", "9:00 AM")]},
    sender="VK-CEBILL", msgs=[("Electricity bill for Nov: Rs 1,284 for consumer 220145789 is due on "
                               "20-11-2026. Pay via PayQuick to avoid late fee.", "9:00 AM")])
add("m05", "sms", {"msgs": [("Your parcel AWB 7788123 has been delivered. Received by: security.", "4:40 PM")]},
    sender="BT-QKSHIP", msgs=[("Your parcel AWB 7788123 is out for delivery today. Agent Vikas: 98xxxxxx45", "9:20 AM")])
add("x09", "sms", {"msgs": [("PNR 4521876630: WL 12, chart not prepared.", "5:00 PM")]},
    sender="VM-RLBOOK", msgs=[("PNR 4521876630, Train 12952: CNF B2 34. Chart prepared. Happy journey!", "6:00 PM")])

# ---------------------------------------------------------------- sheets (desktop)
add("h01", "sheet", {"file": "Budget Oct 2026", "rows": [["Rent", 9500], ["Food", 5100], ["Total", 16300]]},
    file="Monthly budget Nov 2026", cols=["Item", "Amount (Rs)", "Notes"],
    rows=[["Rent", 9500, "paid 3 Nov"], ["Food", 4200, ""], ["Travel", 1500, "metro + auto"],
          ["Internet", 699, ""], ["Total", 15899, ""]])
add("h02", "sheet", {"file": "Marks CSE-3A", "cols": ["Name", "Mid-sem", "Quiz"],
                     "rows": [["Aman", 38, 9], ["Riya", 41, 10], ["Kunal", 29, 7]]},
    file="Attendance CSE-3A", cols=["Name", "Attendance %", "Status"], hard="tall",
    rows=[["Aman", "82%", "OK"], ["Kunal", "68%", "Below 75%"], ["Naman", "91%", "OK"],
          ["Riya", "73%", "Below 75%"]])
add("h03", "sheet", {"file": "Goa trip expenses", "rows": [["Shack stay", "Riya", 8000], ["Scooter rent", "Aman", 2400]]},
    file="Manali trip expenses", cols=["Expense", "Paid by", "Amount"],
    rows=[["Volvo bus", "Naman", 7200], ["Snow Crest Cottage", "Aman", 4800], ["Food", "Riya", 5100],
          ["Solang valley activities", "Kunal", 2100]])
add("h04", "sheet", {"file": "Hackathon tracker", "cols": ["Event", "Date", "Result"],
                     "rows": [["CodeSprint", "21 Nov", "2nd"], ["BuildFest", "5 Oct", "Finalist"]]},
    file="Job applications tracker", cols=["Company", "Role", "Status"],
    rows=[["BrightLoop", "SWE Intern", "Offer"], ["Quanta Labs", "SWE Intern", "Rejected"],
          ["Nimbus Data", "Data Analyst Intern", "OA on 15 Nov"], ["Kite Systems", "Backend Intern", "Applied"]])
add("h05", "sheet", {"file": "Diet log", "cols": ["Meal", "Food", "Protein (g)"],
                     "rows": [["Breakfast", "Oats + milk", 14], ["Lunch", "Dal rice", 18]]},
    file="Gym log", cols=["Exercise", "Sets x reps", "Weight (kg)"], dark=True,
    rows=[["Bench press", "4 x 8", 50], ["Squats", "4 x 10", 70], ["Deadlift", "3 x 5", 90],
          ["Pull-ups", "3 x 6", "body"]])

# ---------------------------------------------------------------- docs and pages (desktop)
add("r01", "doc", {"title": "How to change the dev server port in Vite",
                   "paras": ["Open vite.config.js and set server.port to the port you want, for example 5174."]},
    site="devnotes.example", title="Fix: port 3000 already in use on Windows", byline="5 min read",
    paras=["Another process is still listening on the port. Find it with:", "netstat -ano | findstr :3000",
           "Then stop it using the PID from the last column:", "taskkill /PID 18244 /F"])
add("r02", "doc", {"title": "Internship policy 2027 batch",
                   "paras": ["Students may take one internship of up to 6 months in semester 8."]},
    site="placements.northfield.example", title="Placement eligibility criteria, 2027 batch",
    paras=["Minimum 7.0 CGPA with no active backlogs at the time of the drive.",
           "A student who accepts one offer cannot sit for another company unless the CTC is 1.5x higher."])
add("r03", "doc", {"title": "Conda environments", "paras": ["conda create -n ml python=3.11",
                                                            "conda activate ml"]},
    site="docs.example", title="Python virtual environments", hard="tall",
    paras=["Create one per project so packages do not clash.", "python -m venv .venv",
           "Activate it on Windows with .venv\\Scripts\\activate", "Then pip install -r requirements.txt"])
add("r04", "doc", {"title": "Library rules", "paras": ["Silence must be kept. Books can be issued for 14 days.",
                                                       "Fine for late return is Rs 20 per day."]},
    site="northfield.example", title="Hostel rules and timings", hard="blur",
    paras=["In-time for all residents is 9:30 PM.", "Guests are not allowed in rooms after 7 PM.",
           "Breaking the rules leads to a fine of Rs 500."])
add("r05", "doc", {"title": "Cold coffee", "paras": ["Blend 1 cup cold milk, 2 tsp coffee, sugar and ice."]},
    site="recipes.example", title="Masala chai",
    paras=["Boil 1 cup water with crushed ginger and 2 cardamom pods.",
           "Add 1 cup milk, 2 tsp tea leaves and sugar. Boil for 5 minutes and strain."])
add("x08", "doc", {"title": "Bus timetable - route 45", "paras": ["Indirapuram to College: 7:00 AM, 7:30 AM."]},
    site="transport.northfield.example", title="Bus timetable - route 33",
    paras=["Sector 62 to College: 7:10 AM, 7:40 AM, 8:10 AM.", "College to Sector 62: 4:15 PM, 5:30 PM."])

# ---------------------------------------------------------------- misc cards
add("x01", "kv", {"rows": [("Roll no.", "2200291530047"), ("Exam", "Mid-sem, Data Structures"),
                           ("Centre", "Block A, Room 105"), ("Date", "18 Sep 2026, 10:00")]},
    brand="Northfield Institute of Technology", sub="Admit card",
    rows=[("Roll no.", "2200291530047"), ("Exam", "End-sem, Compiler Design"), ("Centre", "Block C, Room 210"),
          ("Date", "02 Dec 2026, 10:00")])
add("x02", "kv", {"rows": [("Semester", "4"), ("SGPA", "7.90"), ("CGPA", "8.06")]},
    brand="Northfield Institute of Technology", sub="Result",
    rows=[("Semester", "5"), ("SGPA", "8.42"), ("CGPA", "8.15"), ("Result", "Passed in all subjects")])
add("x03", "kv", {"hero": "Sunny", "amount": "31°C", "hero_sub": "Delhi", "rows": [("AQI", "120 Moderate")]},
    brand="SkyCast", sub="Weather", phone=True, hero="Fog", amount="14°C", hero_sub="Noida",
    rows=[("AQI", "312 Very poor"), ("Humidity", "88%"), ("Wind", "6 km/h")])
add("x04", "kv", {"brand": "Central Library", "sub": "Library card",
                  "rows": [("Member ID", "LIB-55210"), ("Valid till", "31 Jul 2027")]},
    brand="FitZone Gym", sub="Membership", phone=True,
    rows=[("Member ID", "FZ-20917"), ("Plan", "6 months"), ("Valid till", "31 Mar 2027")])
add("x05", "kv", {"brand": "Airport Free Wi-Fi", "rows": [("Network", "AIRPORT_FREE"), ("Login", "OTP on mobile")]},
    brand="BrewBean Cafe", sub="Guest Wi-Fi", phone=True,
    rows=[("Network", "BrewBean_Guest"), ("Password", "latte2026"), ("Valid", "2 hours")])
