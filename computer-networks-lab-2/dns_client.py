# dns_client.py
import dns.resolver

def main():
    domain = "example.com"
    log_file = "dns_results.txt"

    try:
        with open(log_file, "w") as f:
            # A record
            ans = dns.resolver.resolve(domain, "A")
            for ip in ans:
                line = f"A record: {ip}\n"
                print(line.strip())
                f.write(line)

            # MX record
            ans = dns.resolver.resolve(domain, "MX")
            for mx in ans:
                line = f"MX record: {mx}\n"
                print(line.strip())
                f.write(line)

            # CNAME record
            try:
                ans = dns.resolver.resolve(domain, "CNAME")
                for cname in ans:
                    line = f"CNAME record: {cname}\n"
                    print(line.strip())
                    f.write(line)
            except:
                print("No CNAME record found.")

        print(f"\nResults saved to {log_file}")

    except Exception as e:
        print("DNS Error:", e)

if __name__ == "__main__":
    main()
